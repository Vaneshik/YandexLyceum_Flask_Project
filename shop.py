from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from db_data import db_session
from db_data.products import Product
from forms.product import *
import stripe

shop = Blueprint('shop', __name__)
publishable_key = 'pk_test_51IivHBL5CLahxtbO4F6MO50SssgTZPNP85x7Fdmo4PUiHWeFy1AWTcEuvLFLmQf9cRKOa6LCod6ATXeck0yqhbuM00C31c2qnp'


def get_best_prods(n, category="Акксесуары", page=1):
    db_sess = db_session.create_session()
    q = [db_sess.query(Product).get(i) for i in range(1, n+1)]
    # q = [a[i] for i in range(1 + (page - 1) * 9, 10 + (page - 1) * 9)]
    # print(q)
    return q


@shop.route('/shop', methods=['GET'])
def market():
    prods = get_best_prods(9, category=request.args.get("category"), page=request.args.get("page"))
    return render_template('shop_.html', **{'prod': prods})


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
    user.products.append(prod, amount)
    db_sess.merge(user)
    db_sess.commit()
    return render_template('added_.html')


@shop.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'GET':
        user = current_user
        prods = user.products
        price = sum(prod[0].price * prod[1] for prod in prods)
        return render_template('chechout_.html', **{'prods': prods, 'price': price})
    else:
        prods = current_user.products
        price = sum(prod[0].price * prod[1] for prod in prods)
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=price * 100,
            currency='rub',
            description='Buy Charge'
        )
        return render_template('charge_.html', amount=price, key=publishable_key)
