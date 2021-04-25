import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

from data import db_session
from data.exercises import Exercises
from data.users import User


def main():
    vk_session = vk_api.VkApi(
        token=open('data/token.txt', mode='r').read())
    longpoll = VkBotLongPoll(vk_session, '203859351')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if event.obj.message['text'].lower() == 'дай дз':
                db_sess = db_session.create_session()
                if event.obj.message['from_id'] in [_[0] for _ in db_sess.query(User.vk_id).filter(
                        User.teacher == False).all()]:
                    grade = db_sess.query(User.grade).filter(
                        User.vk_id == event.obj.message['from_id']).first()[0]
                    if db_sess.query(Exercises.homework).filter(
                            Exercises.class_id == grade).all():
                        today = datetime.date.today()
                        tomorrow = today + datetime.timedelta(days=1)
                        for t_id, hom, date in db_sess.query(
                                Exercises.teacher_id,
                                Exercises.homework, Exercises.date).filter(
                            Exercises.class_id == grade, Exercises.date == tomorrow).all():
                            subject = db_sess.query(User.subject).filter(
                                User.id == t_id).all()
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Задание за {date} по предмету {subject[0][0]} :",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"{hom}",
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Отдыхайте вам ничего не задали",
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Вы не зарегистрированны в системе",
                                     random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Неизвестная команда",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    db_session.global_init("db/school8.db")
    main()
