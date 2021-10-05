from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        page_title = "Почтовый помошник"
        address = "yashkins@yandex.ru"
        return render_template('index.html',page_title=page_title, address=address)
    return app
