import hashlib

from flask import Flask
from waitress import serve
from forms.form_user import User_reg
from data import db_session
from flask import request, redirect, render_template
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['POST', 'GET'])
def func():
    form = User_reg()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # проверка уникальности логина
        user = User()
        user.name = form.name.data
        user.login = form.login.data
        user.teacher = form.teacher.data
        user.hashed_password = hashlib.sha512(form.password.data.encode('utf-8')).hexdigest()
        print(form.password.data)
    return render_template("register.html", form=form, title='Регистрация')


if __name__ == '__main__':
    db_session.global_init("db/school.db")
    app.run(host='127.0.0.1', port=9998)
