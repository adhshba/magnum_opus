from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired


class User_reg(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    teacher = BooleanField('Я учитель')
    submit = SubmitField('Зарегистрироваться')


class User_authorize(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class Join_to_class(FlaskForm):
    class_id = StringField('ID класса', validators=[DataRequired()])
    submit = SubmitField('Присоединиться')


class Edit_name(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class Edit_surname(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class Class_num_add(FlaskForm):
    class_num = StringField('Номер класса', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class Add_class(FlaskForm):
    add_class = StringField('ID класса', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Subject(FlaskForm):
    subject = StringField('Предмет', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Edit_mark(FlaskForm):
    mark = IntegerField('Оценка', validators=[DataRequired()])
    submit = SubmitField('Редактировать')


class Delete_mark(FlaskForm):
    submit = SubmitField('Удалить')


class Edit_homework(FlaskForm):
    text = TextAreaField('Отредактируйте домашнее задание', validators=[DataRequired()])
    submit = SubmitField('Редактировать')


class Add_homework(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()])
    text = TextAreaField('Домашнее задание', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Create_test(FlaskForm):
    kolvo = IntegerField('Количество вопросов в тесте', validators=[DataRequired()])
    submit = SubmitField('Далее')


class Test(FlaskForm):
    question = StringField('Вопрос', validators=[DataRequired()])
    true_answer = StringField('Правильный ответ', validators=[DataRequired()])
    answer2 = StringField('Неправильный ответ', validators=[DataRequired()])
    answer3 = StringField('Неправильный ответ', validators=[DataRequired()])
    answer4 = StringField('Неправильный ответ', validators=[DataRequired()])
