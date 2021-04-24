from flask import Flask
from db_data.app_file import set_app, set_login_manager
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager(app)
set_app(app)
set_login_manager(login_manager)


def get_login_manager():
    return login_manager


def get_app():
    return app
