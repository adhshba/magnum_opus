from flask import Flask
import hashlib
from flask_login import login_user
from waitress import serve
from data import db_session
from data.users import User
from forms.form_user import User_reg, User_authorize
from flask import request, redirect, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['POST', 'GET'])
def register():
    form = User_reg()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        user = User()
        user.name = form.name.data
        user.login = form.login.data
        user.teacher = form.teacher.data
        user.hashed_password = hashlib.sha512(form.password.data.encode('utf-8')).hexdigest()
    return render_template("register.html", form=form, title='Регистрация')


@app.route('/authorize', methods=['POST', 'GET'])
def authorize():
    form = User_authorize()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and hashlib.sha512(form.password.data.encode('utf-8')).hexdigest() == user.hashed_password:
            login_user(user)
            return redirect("/go")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("authorize.html", form=form, title='Вход')


@app.route('/go')
def go():
    return 'ok'


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
