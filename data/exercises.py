import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
import datetime


class Exercises(SqlAlchemyBase):
    __tablename__ = 'exercises'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    class_id = sqlalchemy.Column(sqlalchemy.String)
    homework = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now().date())
    user = orm.relation('User')