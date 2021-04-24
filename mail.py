from flask_mail import Mail, Message
from app_file import get_app


app = get_app()
mail = Mail(app)


def send_email(subject, sender, recipient, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
