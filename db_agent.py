import db_data.db_session as db_session

from db_data.users import User
from db_data.products import Product
from db_data.categories import Category
from db_data.categories_types import Type
from db_data.db_session import create_session


class AddError(Exception):
    pass


def is_aviable(product):
    return create_session().query(Product).filter(Product.name == product).first().is_aviable


def create_product(name, pics, content):
    sess = create_session()
    if not sess.query(Product).filter(Product.name == name).count():
        product = Product()
        product.name = name
        product.pics = pics
        product.content = content
        sess.add(product)
        sess.commit()
        return sess.query(Product).filter(Product.name == name).first().id
    else:
        raise AddError('Invalid name')


def add_to_cart(user, product):
    sess = create_session()
    user = sess.query(User).filter(User.login == user)
    product = sess.query(Product).filter(Product.name == product)
    user.products.add(product)
    product.amount -= 1
    product.is_aviable = (bool(max(0, product.amount)))

    sess.commit()


def remove_from_cart(user, product):
    sess = create_session()
    user = sess.query(User).filter(User.login == user)
    product = sess.query(Product).filter(Product.name == product)
    user.products.remove(product)
    product.amount += 1
    product.is_aviable = (bool(max(0, product.amount)))

    sess.commit()


def get_amount(product):
    sess = create_session()
    product = sess.query(Product).filter(Product.name == product)
    return product.amount


def change_amount(product, new):
    sess = create_session()
    product = sess.query(Product).filter(Product.name == product)
    product.amount = new
    sess.commit()
