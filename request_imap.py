import imaplib
import getpass

mail = imaplib.IMAP4_SSL('imap.yandex.ru')
mail.login('yashkins@yandex.ru', getpass.getpass())
mail.select('inbox')
result, data = mail.uid('search', None, 'ALL')
list_uid = data[0].split()
print(list_uid)