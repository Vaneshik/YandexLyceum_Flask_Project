from flask import Flask, request, render_template
from db_data import db_session
from auth import auth as auth_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'


def main():
    db_session.global_init('db/users.sqlite')
    app.register_blueprint(auth_blueprint)
    app.run()


@app.route('/')
def index():
    return render_template('home_.html')


if __name__ == '__main__':
    main()
