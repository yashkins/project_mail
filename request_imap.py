import base64
import imaplib
import email
import settings


def get_imap(login=None, password=None, date=None):
    password = settings.password
    login = settings.login
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login(login, password)
    mail.select('inbox')
    if not date:
        result, data = mail.uid('search', None, 'ALL')
    else: 
        result, data = mail.uid('search', None, '(SENTSINCE{date})'.format(date=date))
    list_uids = data[0].split()
    return list_uids, mail


def create_dict_name_uid():    
    dict_name_uid = {}
    list_uids, mail = get_imap()
    for id in list_uids:
        result, data = mail.uid('fetch', id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        name, adress = email.utils.parseaddr(email_message['From'])
        """name = base64.b64decode(name.encode()).decode(errors='ignore') если разберусь с кодировкой, то добавлю эту строку"""
        dict_name_uid[adress] = dict_name_uid.get(adress, []) + [id]
        
    return dict_name_uid


def delete(list_uids, mail):
    for uid in list_uids:
        mail.store(uid, '+FLAGS', '\\Deleted')
        mail.expunge()
        



