import flask
from flask import request, jsonify
import hashlib
from . import db_session
from .users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/authorize', methods=['POST'])
def check_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == request.json['login']).first()
    if user and hashlib.sha512(request.json['password'].encode('utf-8')).hexdigest() \
            == user.hashed_password:
        x = True if user.teacher else False
        db_sess.commit()
        return jsonify({'success': 'OK', 'id': user.id})
    db_sess.commit()
    return jsonify({'error': 'not correct data'})


@blueprint.route('/api/info', methods=['POST'])
def information():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == request.json['login']).first()
    if user and hashlib.sha512(request.json['password'].encode('utf-8')).hexdigest() \
            == user.hashed_password:
        if user.teacher:
            classes = []
            for i in user.classes.split(';'):
                class_ = db_sess.query(User). \
                    filter(User.grade_for_teacher == i).first()
                classes.append(class_.class_num)
            info = {'surname': user.surname,
                    'name': user.name,
                    'classes': classes,
                    'grade_for_stud': user.grade,
                    'grade_for_teacher': user.grade_for_teacher,
                    'class_num': user.class_num,
                    'subject': user.subject}
        else:
            info = {'surname': user.surname,
                    'name': user.name,
                    'grade': user.grade,
                    'class_num': user.class_num}
        db_sess.commit()
        return jsonify(info)
    db_sess.commit()
    return jsonify({'error': 'not correct data'})