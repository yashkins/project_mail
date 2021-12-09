from flask import Flask, app, render_template, request
from webapp.request_imap import get_imap, create_dict_name_uid, delete
import os

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        global mail
        page_title = "Почтовый помошник"
        address = "yashkins@yandex.ru/Входящие"
        list_uids, mail = get_imap()
        dict_name_uid, dict_name_len, mail = create_dict_name_uid(list_uids, mail)
        with open('db.txt', 'w') as db:
            for k,v in dict_name_uid.items():
                db.write(f"{k} {','.join(map(str,v))}\n")
        return render_template('index.html', page_title=page_title, address=address, dict_name_len=dict_name_len, mail=mail)

    @app.route('/del/', methods=['GET','POST'])
    def remove():
        page_title = "Почтовый помошник"
        address = "yashkins@yandex.ru/Входящие"
        dict_keys = request.form
        dict_name_len, list_uids = {}, []
        with open('db.txt') as db:
            with open('db1.txt', 'w') as db1:
                for row in db.readlines():
                    row_sp = row.split()
                    if row_sp[0] in dict_keys:
                        list_uids += [i[2:-1].encode() for i in row_sp[1].split(',')]
                    else:
                        dict_name_len[row_sp[0]] = len(row_sp[1].split(','))
                        db1.write(row)
        try:
            delete(list_uids,mail)
        except: 
            return render_template('index.html',page_title=page_title, address=address, dict_name_len=dict_name_len, mail=None)
        os.remove('db.txt')
        os.rename('db1.txt','db.txt')
        dict_name_len_sort = dict(sorted(dict_name_len.items(), key=lambda x:x[1],reverse=True))
        return render_template('index.html',page_title=page_title, address=address, dict_name_len=dict_name_len_sort, mail=mail)
    return app

