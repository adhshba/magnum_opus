import flask
from flask import request, jsonify
import hashlib
from . import db_session
from .marks import Marks
from .users import User

blueprint = flask.Blueprint('marks_api', __name__, template_folder='templates')


@blueprint.route('/api/marks_for_student', methods=['POST'])
def marks_for_student():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == request.json['login']).first()
    if user and hashlib.sha512(request.json['password'].encode('utf-8')).hexdigest() \
            == user.hashed_password:
        student_marks = db_sess.query(Marks).filter(Marks.user_id == user.id) \
            .order_by(Marks.teacher_id).all()
        dates = sorted([i.date for i in student_marks])
        dates = ['Предмет'] + dates
        dict_marks = {}
        for i in student_marks:
            subject = db_sess.query(User).filter(User.id == i.teacher_id).first().subject
            if subject not in dict_marks:
                dict_marks[subject] = [{'date': i.date, 'mark': i.mark}]
            else:
                dict_marks[subject].append({'date': i.date, 'mark': i.mark})
        for key, val in dict_marks.items():
            sr_ball = [int(i['mark']) for i in val]
            dict_marks[key].append({'sr_ball': sum(sr_ball) / len(sr_ball)})
        dates.append('Средний балл')
        db_sess.commit()
        return jsonify({'dict_marks': dict_marks, 'dates': dates})
    db_sess.commit()
    return jsonify({'error': 'not correct data'})


@blueprint.route('/api/marks_for_teacher', methods=['POST'])
def marks_for_teacher():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == request.json['login']).first()
    if user and hashlib.sha512(request.json['password'].encode('utf-8')).hexdigest() \
            == user.hashed_password:
        pass

# @blueprint.route('/api/marks')