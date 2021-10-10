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
    list_uid = data[0].split()
    dict_name_uid = {}
    for id in list_uid:
        result, data = mail.uid('fetch', id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        name = email.utils.parseaddr(email_message['From'])
        name = name[0]
        dict_name_uid = dict_name_uid[name].get(name, []).append(id)
    return dict_name_uid

    

