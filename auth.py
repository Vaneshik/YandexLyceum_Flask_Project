from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user
from db_data import db_session
from db_data.users import User
from forms.user import RegisterForm, LoginForm
from app_file import get_app
from mail import send_confirmation_email


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.name.data).first()
        print(db_sess.query(User).first().login)
        print(form.name.data)
        print(db_sess.query(User).first().login == form.name.data)
        if not user:
            return render_template('login_.html', title='Вход', form=form)
        if user.check_password(form.password.data) and user.is_confirmed != 1:
            send_confirmation_email(user)
            return render_template('please_confirm_.html', title='Confirm')
        elif user.check_password(form.password.data):
            return redirect(url_for(get_app().index))
    return render_template('login_.html', title='Вход', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup_.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).count() or \
                db_sess.query(User).filter(User.login == form.name.data).count():
            return render_template('signup_.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.name.data,
            email=form.email.data,
            is_admin=False
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('signup_.html', title='Регистрация', form=form)


@auth.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return render_template('expired_.html')
    db_sess = db_session.create_session()
    user.is_confirmed = True
    db_sess.commit()
    login_user(user)
    return render_template('confirmed_.html')
