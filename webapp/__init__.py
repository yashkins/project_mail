from flask import Flask, render_template
from webapp.request_imap import get_imap, create_dict_name_uid


def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        page_title = "Почтовый помошник"
        address = "yashkins@yandex.ru/Входящие"
        #list_uids, mail = get_imap()
        #dict_name_uid = create_dict_name_uid(list_uids, mail)
        #list_name_count = [(k,len(v)) for k,v in dict_name_uid.items()]
        list_name_count = [('vk',26),('odnoklassniki',24),('facebooke',20)]
        return render_template('index.html',page_title=page_title, address=address, list_name_count=list_name_count)
    return app
