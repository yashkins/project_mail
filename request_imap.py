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
        name = email.utils.parseaddr(email_message['From'])
        name = base64.b64decode(name[0][:-1].encode()).decode(errors='ignore')
        dict_name_uid[name] = dict_name_uid.get(name, set()).add(id)
        break
    return dict_name_uid

for k,v in create_dict_name_uid().items():
    print(k,v)

    

