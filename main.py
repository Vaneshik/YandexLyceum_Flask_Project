from db_data import db_session
from auth import auth as auth_blueprint
from shop import shop as shop_blueprint
import app_file

app = app_file.get_app()
app.config['SECRET_KEY'] = '123'


def main():
    db_session.global_init('db/shop.sqlite')
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(shop_blueprint)
    app.run()


if __name__ == '__main__':
    main()
