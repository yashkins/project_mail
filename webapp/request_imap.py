import base64
import datetime 
import imaplib
import email
from webapp import settings 
import threading
from collections import deque


def get_imap(login=None, password=None, date=None):
    password = settings.password
    login = settings.login
    try:
        mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    except:
        return [], None
    mail.login(login, password)
    mail.select('Inbox')
    if not date:
        result, data = mail.uid('search', None, 'ALL')
    else:
        result, data = mail.uid('search', None, '(SINCE {date})'.format(date=date))
    list_uids = data[0].split()
    return list_uids, mail

def parser(outque, data, uids, i):
    raw_email = data[i][1]
    email_message = email.message_from_bytes(raw_email)
    try:
        name, adress = email.utils.parseaddr(email_message['From'])
    except TypeError:
        print("empty header", "Номер письма: ", uids[i])
        return
    outque.append((adress,uids[i]))


def create_dict_name_uid(list_uids, mail):
    dict_name_uid = {}
    for i in range(0,len(list_uids),500):
        uids = list_uids[i:i+500]
        try:
            result, data = mail.uid('fetch', b','.join(uids), '(RFC822.HEADER)')
        except:
            return {}, None
        data = data[::2]
        outque = deque()
        list_join = []
        for i in range(len(data)):
            th = threading.Thread(target=parser,args=(outque, data, uids, i,))
            list_join.append(th)
            th.start()
        for i in list_join:
            i.join()
        while True:
            try:
                adress, uid = outque.popleft()
            except IndexError:
                break
            dict_name_uid[adress] = dict_name_uid.get(adress, []) + [uid.decode()]
    return dict_name_uid, mail


def delete(list_uids, mail):
    for uid in list_uids:
        mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
    mail.expunge()


