import db_data.db_session as db_session

from db_data.users import User
from db_data.products import Product
from db_data.categories import Category
from db_data.categories_types import Type


class AddError(Exception):
    pass


def init():
    db_session.global_init("db/shop.db")
    global sess
    sess = db_session.create_session()


def is_aviable(product):
    return sess.query(Product).filter(Product.name == product).first().is_aviable


def create_user(login, email, password):
    if not sess.query(User).filter(User.login == login | User.email == email).count():
        user = User()
        user.login = login
        user.email = email
        user.hashed_password = password
        sess.add(user)
        sess.commit()
        return sess.query(User).filter(User.login == login).first().id
    elif sess.query(User).filter(User.login == login).count():
        raise AddError('Invalid login')
    else:
        raise AddError('Invalid email')


def change_password(login, old, new):
    user = sess.query(User).filter(User.login == login).first()
    if user.hashed_password == old:
        user.hashed_password = new
        return True
    return False


def authorize(login, password):
    user = sess.query(User).filter(User.login == login).first()
    return user.hashed_password == password


def create_product(name, pics, content):
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
    user = sess.query(User).filter(User.login == user)
    product = sess.query(Product).filter(Product.name == product)
    user.products.add(product)
    product.amount -= 1
    product.is_aviable = (bool(max(0, product.amount)))

    sess.commit()


def remove_from_cart(user, product):
    user = sess.query(User).filter(User.login == user)
    product = sess.query(Product).filter(Product.name == product)
    user.products.remove(product)
    product.amount += 1
    product.is_aviable = (bool(max(0, product.amount)))

    sess.commit()


def get_amount(product):
    product = sess.query(Product).filter(Product.name == product)
    return product.amount


def change_amount(product, new):
    product = sess.query(Product).filter(Product.name == product)
    product.amount = new
    sess.commit()


if __name__ == '__main__':
    init()
