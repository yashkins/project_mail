from flask import Flask, app, render_template, request
from webapp.request_imap import get_imap, create_dict_name_uid, delete
from webapp.DataBase import DataBase


def create_app():
    app = Flask(__name__)
    obj_db = DataBase()
    date = obj_db.select()
    list_uids, mail = get_imap(date=date)
    dict_name_uid, mail = create_dict_name_uid(list_uids, mail)

    @app.route('/')
    def index():
        page_title = "Почтовый помошник"
        address = "yashkins@yandex.ru/Входящие"
        obj_db.insert(dict_name_uid)
        return render_template('index.html', page_title=page_title, address=address, dict_name_len=obj_db.dict_name_len, mail=mail)    

    @app.route('/del/', methods=['GET','POST'])
    def remove():
        page_title = "Почтовый помошник"
        address = "yashkins@yandex.ru/Входящие"
        dict_keys = request.form
        obj_db.delete(dict_keys, mail)
        return render_template('index.html',page_title=page_title, address=address, dict_name_len=obj_db.dict_name_len, mail=obj_db.mail)
        
    return app

