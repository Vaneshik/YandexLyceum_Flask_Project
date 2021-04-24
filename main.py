from flask import Flask, request, render_template
from db_data import db_session
from auth import auth as auth_blueprint
import app_file
import subprocess
from threading import Thread

app = app_file.get_app()
app.config['SECRET_KEY'] = '123'
app.config['ADMINS'] = ['denis.r.vasiuk@gmail.com']


def run_mail():
    subprocess.call(['mail_server.bat'])


#  run mail server
Thread(target=run_mail, args=()).start()


def main():
    db_session.global_init('db/users.sqlite')
    app.register_blueprint(auth_blueprint)
    app.run()


@app.route('/')
def index():
    return render_template('home_.html')


if __name__ == '__main__':
    main()
