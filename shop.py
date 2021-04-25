from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from db_data import db_session
from db_data.products import Product
from forms.product import *


shop = Blueprint('shop', __name__)


def get_best_prods(n):
    return []


@shop.route('/', methods=['GET'])
def index():
    prods = get_best_prods(5)
    return render_template('home_.html', **{'prods': prods})


def search_in_db(name):
    words = name.split()
    for i in words:
        if not i:
            words.pop(words.index(''))
    db_sess = db_session.create_session()
    if not words:
        return db_sess.query(Product).all()
    q = db_sess.query(Product).filter(Product.name.like(f'%{words[0]}%'))
    for i in words[1:]:
        q = q.filter(Product.name.like(f'%{i}%'))
    return q


@shop.route('/search/<name>', methods=['GET'])
def search(name):
    prods = search_in_db(name)
    return render_template('search_.html', **{'prods': prods})


@shop.route('/product/<id>', methods=['GET'])
def product(id):
    db_sess = db_session.create_session()
    prod = db_sess.query(Product).filter(Product.id == id).first()
    return render_template('product_.html', **{'prod': prod})


@shop.route('/product/<id>', methods=['POST'])
@login_required
def add_to_cart(id):
    form = ProductForm()
    db_sess = db_session.create_session()
    prod = db_sess.query(Product).filter(Product.id == id).first()
    user = current_user
    amount = form.amount.data
    user.products.append(prod)
    # set amount somehow
    db_sess.merge(user)
    db_sess.commit()
    return render_template('added_.html')


@shop.route('/checkout')
def checkout():
    user = current_user
