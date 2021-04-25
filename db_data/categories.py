import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

association_table = sqlalchemy.Table(
    'categories_to_products',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('products', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column('categories', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             primary_key=True, nullable=False, unique=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("types.id"))
    type = orm.relation('Type')
