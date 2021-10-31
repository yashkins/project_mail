import base64
import datetime 
import imaplib
import email
from webapp import settings 



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


def create_dict_name_uid(list_uids, mail):    
    dict_name_uid = {}
    if not list_uids:
        return dict_name_uid
    for i in range(0,len(list_uids),20):
        uids = list_uids[i:i+20]  
        result, data = mail.uid('fetch', b','.join(uids), '(RFC822.HEADER)')
        for key, elem in enumerate(data[::2]):
            raw_email = elem[1]
            email_message = email.message_from_bytes(raw_email)
            name, adress = email.utils.parseaddr(email_message['From'])
            """name = base64.b64decode(name.encode()).decode(errors='ignore') если разберусь с кодировкой, то добавлю эту строку"""
            dict_name_uid[adress] = dict_name_uid.get(adress, []) + [uids[key]] 
        break 
    return dict_name_uid


def delete(list_uids, mail):
    for uid in list_uids:
        mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
    mail.expunge()


if __name__ == "__main__":       
    mail, list_uids = get_imap()
    dict_name_uids = create_dict_name_uid(mail, list_uids)
    for k,v in dict_name_uids.items():
        print(k,len(v))