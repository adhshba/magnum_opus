import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Tests(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # id теста
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    students = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=True)
    # название теста
    # shelf_life = sqlalchemy.Column(sqlalchemy.DATE, nullable=True)
    # дата до которой тест актуален при совпадении с датой в настоящее время
    # удалять все связвные вопросы в таблице question ,а после
    # и запись в этой таблице, это надо куда нибудь засунуть в ввиде
    # автоматической проверки и привязать к дате на сервере
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # дата создания теста