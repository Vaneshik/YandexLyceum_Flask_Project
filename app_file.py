from flask import Flask

app = Flask(__name__)


def get_app():
    return app
