from db_data import db_session
from auth import auth as auth_blueprint
# from auth import signup as signup_blueprint
from shop import shop as shop_blueprint
import app_file
import stripe
from flask import render_template

app = app_file.get_app()
app.config['SECRET_KEY'] = '123'
stripe.api_key = 'sk_test_51IivHBL5CLahxtbOHR926HSV6OgysnJaRjirl0624Mp3J88RitAqiVV7C3BThXcNqsO8dt2Twer4jqf9YbvbzD6200AX0LiSDb'


@app.route("/")
def index():
    return render_template('home_.html')


# @app.route("/login")
# def login():
#     return render_template("login.html")


@app.route("/signup")
def register():
    return render_template("signup.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


# @app.route("/cart")
# def cart():
#     return render_template("cart.html")


@app.route("/about")
def about():
    return render_template("about_.html")


@app.route("/user")
def admin():
    return render_template("user.html")


@app.route("/item")
def item():
    return render_template("item.html")


def main():
    db_session.global_init('db/shop.sqlite')
    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(auth_blueprint)
    # app.register_blueprint(shop_blueprint)
    app.run()


if __name__ == '__main__':
    main()
