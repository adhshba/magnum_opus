from flask import Flask
from waitress import serve
from forms.form_user import User_reg
from flask import request, redirect, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['POST', 'GET'])
def func():
    form = User_reg()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # проверка уникальности логина
    return render_template("register.html", form=form, title='Регистрация')


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
