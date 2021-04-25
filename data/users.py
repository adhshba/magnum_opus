import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, default="")
    grade = sqlalchemy.Column(sqlalchemy.String, default='')
    classes = sqlalchemy.Column(sqlalchemy.String, default='')
    grade_for_teacher = sqlalchemy.Column(sqlalchemy.String, default='')
    class_num = sqlalchemy.Column(sqlalchemy.String, default='')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, default='')
    marks = orm.relation("Marks", back_populates='user')