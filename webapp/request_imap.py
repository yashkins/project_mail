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
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
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
    if not list_uids:
        return dict_name_uid
    for i in range(0,20,10):
        uids = list_uids[i:i+10]
        result, data = mail.uid('fetch', b','.join(uids), '(RFC822.HEADER)')
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
            dict_name_uid[adress] = dict_name_uid.get(adress, []) + [uid]
    dict_name_len = {k:len(v) for k,v in dict_name_uid.items()}
    tuple_sort = sorted(dict_name_len.items(), key=lambda x:x[1],reverse=True)
    dict_name_len = dict(tuple_sort)
    return dict_name_uid, dict_name_len


def delete(list_uids, mail):
    for uid in list_uids:
        mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
    mail.expunge()


