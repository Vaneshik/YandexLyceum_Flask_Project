import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Type(SqlAlchemyBase):
    __tablename__ = 'types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    categories = orm.relation("Category", back_populates='type')