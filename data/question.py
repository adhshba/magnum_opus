import sqlalchemy
from sqlalchemy.orm import relationship, backref

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'question'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # вопрос
    answer_options = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # строка с вариантами ответа с разделением черех '&'
    correct_answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # номер правильного ответа как число
    id_test = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("tests.id"),
                                nullable=True)
    # номер теста к которому принадлежит задание
    # связан с id в таблице tests
    # при отображении теста в общем вопросы будут выводится
    # в порядке возрастания id и пронумерованны
    test = relationship("Tests", foreign_keys=id_test,
                        backref=backref("question"))
    # стандартная связка