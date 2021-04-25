from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user
from db_data import db_session
from db_data.users import User
from forms.user import RegisterForm, LoginForm
from app_file import get_app, get_login_manager
import mail


auth = Blueprint('auth', __name__)
login_manager = get_login_manager()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.name.data).first()
        if not user:
            return render_template('login_.html', title='Вход', form=form)
        if user.check_password(form.password.data) and user.is_confirmed != 1:
            mail.send_confirmation_email(user)
            return render_template('please_confirm_.html', title='Confirm')
        elif user.check_password(form.password.data):
            login_user(user)
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
    logout_user()
    id = User.verify_token(token)
    db_sess = db_session.create_session()
    user = load_user(id)
    if not user:
        return render_template('expired_.html')
    user.is_confirmed = True
    db_sess.merge(user)
    db_sess.commit()
    login_user(user)
    return render_template('confirmed_.html')
