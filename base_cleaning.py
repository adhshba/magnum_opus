from datetime import datetime

from data import db_session
from data.question import Question
from data.tests import Tests
from data.exercises import Exercises

import schedule
import time


def cleaning():
    db_sess = db_session.create_session()
    current_date = datetime.now().date()
    db_sess.query(Exercises).filter(Exercises.date <= current_date).delete()
    for i in db_sess.query(Tests.id).filter(Tests.shelf_life <= current_date).all():
        db_sess.query(Question).filter(Question.id_test == i[0]).delete()
    db_sess.query(Tests).filter(Tests.shelf_life <= current_date).delete()
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/school8.db")
    schedule.every().day.at("18:00").do(cleaning)
    while True:
        schedule.run_pending()
        time.sleep(1)
