import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Type(SqlAlchemyBase):
    __tablename__ = 'types'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             primary_key=True, nullable=False)

    categories = orm.relation("Category", back_populates='type')
