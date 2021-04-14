import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
