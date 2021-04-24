import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from time import time
import jwt
from app_file import get_app
from werkzeug.security import generate_password_hash, check_password_hash
from app_file import get_login_manager


login_manager = get_login_manager()


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    is_confirmed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    products = orm.relation("Product",
                            secondary="products_to_users",
                            backref="products")

    def get_token(self, expires_in=600):
        tok = jwt.encode(
            {'token': self.id, 'exp': time() + expires_in},
            get_app().config['SECRET_KEY'], algorithm='HS256')
        return tok

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, get_app().config['SECRET_KEY'],
                            algorithms=['HS256'])['token']
        except Exception:
            return
        return id

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
