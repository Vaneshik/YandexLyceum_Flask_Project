from flask_mail import Mail, Message
from flask import render_template
from app_file import get_app
from threading import Thread


app = get_app()
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipient, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_confirmation_email(user):
    token = user.get_reset_password_token()
    send_email('Confirm your account',
               sender=app.config['ADMINS'][0],
               recipient=user.email,
               text_body=render_template('confirmation_mail.txt',
                                         user=user, token=token),
               html_body=render_template('confirmation_mail.html',
                                         user=user, token=token))
