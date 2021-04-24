from flask import Flask
from db_data.app_file import set_app

app = Flask(__name__)
set_app(app)


def get_app():
    return app
