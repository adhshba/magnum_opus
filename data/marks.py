import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
import datetime


class Marks(SqlAlchemyBase):
    __tablename__ = 'marks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now().date())
    user = orm.relation('User')