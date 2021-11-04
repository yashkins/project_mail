import base64
import datetime
import imaplib
import email
import threading
from collections import deque
from webapp import settings
import time


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
    name, adress = email.utils.parseaddr(email_message['From'])
    outque.append((adress,uids[i]))


def create_dict_name_uid(list_uids, mail):
    dict_name_uid = {}
    if not list_uids:
        return dict_name_uid
    for i in range(0,800,100):
        uids = list_uids[i:i+100]
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
    return dict_name_uid


def delete(list_uids, mail):
    for uid in list_uids:
        mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
    mail.expunge()


if __name__ == "__main__":
    mail, list_uids = get_imap()
    start = time.time()
    dict_name_uids = create_dict_name_uid(mail, list_uids)
    end = time.time()
    for k,v in dict_name_uids.items():
        print(k,len(v))
    print(sum([len(v) for k,v in dict_name_uids.items()]))
    print(end-start)