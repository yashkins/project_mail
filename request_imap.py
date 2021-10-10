import imaplib
import email
import seting

password = seting.password
mail = imaplib.IMAP4_SSL('imap.yandex.ru')
mail.login('yashkins@yandex.ru', password)
mail.select('inbox')
result, data = mail.uid('search', None, 'ALL')
list_uid = data[0].split()
list_name = []
i = list_uid[0]
result, data = mail.uid('fetch', i, '(RFC822)')
raw_email = data[0][1]
email_message = email.message_from_bytes(raw_email)
name = email.utils.parseaddr(email_message['From'])
list_name.append(name)
print(name[0])

