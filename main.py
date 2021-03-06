from flask import Flask
import hashlib
from random import choice, sample, randint, shuffle
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from waitress import serve
import vk_api
from datetime import datetime
from data import db_session
from data.question import Question
from data.tests import Tests
from data.users import User
from data.marks import Marks
from data.exercises import Exercises
from forms.form_user import User_reg, User_authorize, \
    Join_to_class, Edit_name, Edit_surname, Class_num_add, \
    Add_class, Subject, Edit_mark, Delete_mark, Edit_homework, Add_homework, Create_test, Test
from flask import request, redirect, render_template
import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def generate_password():
    x = choice('abcdefghijkmnpqrstuvwxyz')
    x += choice('ABCDEFGHJKLMNPQRSTUVWXYZ')
    x += choice('23456789')
    p = list('abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    del p[p.index(x[0])]
    del p[p.index(x[1])]
    del p[p.index(x[2])]
    x = list(x)
    k = 15 - 3
    x += sample(p, k=k)
    return ''.join(x)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        logout()
    form = User_reg()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        user_log = db_sess.query(User).filter(User.login == form.login.data).first()
        if user_log:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой логин уже существует!")
        user = User()
        user.name = form.name.data.capitalize()
        user.surname = form.surname.data.capitalize()
        user.login = form.login.data
        if form.teacher.data:
            while True:
                x = generate_password()
                if not db_sess.query(User).\
                        filter((User.grade == x) | (User.grade_for_teacher == x)).first():
                    user.grade = x
                    break
            while True:
                x = generate_password()
                if not db_sess.query(User).\
                        filter((User.grade == x) | (User.grade_for_teacher == x)).first():
                    user.grade_for_teacher = x
                    user.classes = x
                    break
        user.teacher = form.teacher.data
        user.hashed_password = hashlib.sha512(form.password.data.encode('utf-8')).hexdigest()
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=False)
        return redirect('/main_page')
    return render_template("register.html", form=form, title='Регистрация')


@app.route('/authorize', methods=['POST', 'GET'])
def authorize():
    form = User_authorize()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and \
                hashlib.sha512(form.password.data.encode('utf-8')).hexdigest() \
                == user.hashed_password:
            login_user(user, remember=False)
            return redirect('/main_page')
        return render_template('authorize.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Вход')
    return render_template("authorize.html", form=form, title='Вход')


@login_required
@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    message = ''
    html = 'teacher_main_page.html'
    form_class = ''
    form = ''
    grade = True
    form_add_class = ''
    db_sess = db_session.create_session()
    classes = ''
    form_subject = ''
    if not current_user.teacher:
        if not current_user.class_num and current_user.grade:
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            class_num_stud = db_sess.query(User).\
                filter(User.grade == current_user.grade).first().class_num
            if class_num_stud:
                user.class_num = class_num_stud
                db_sess.add(user)
                db_sess.commit()
                return redirect('/main_page')
        html = 'student_main_page.html'
        form = Join_to_class()
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            if db_sess.query(User).filter(User.grade == form.class_id.data,
                                          User.teacher).first():
                user.grade = form.class_id.data
                db_sess.add(user)
                db_sess.commit()
                return redirect('/main_page')
            else:
                message = 'Такого ID класса не существует!'
        if not current_user.grade:
            grade = False
    else:
        classes = db_sess.query(User).\
            filter(User.grade_for_teacher.in_(current_user.classes.split(';'))).all()
        classes = [i.class_num for i in classes]
        form_class = Class_num_add()
        form_subject = Subject()
        if form_subject.validate_on_submit():
            if form_subject.subject.data.isalpha():
                user = db_sess.query(User).filter(User.login == current_user.login).first()
                user.subject = form_subject.subject.data.capitalize()
                db_sess.add(user)
                db_sess.commit()
                return redirect('/main_page')
            else:
                message = 'Введите корректное название предмета'
        if form_class.validate_on_submit():
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            user.class_num = form_class.class_num.data
            db_sess.add(user)
            db_sess.commit()
            return redirect('/main_page')
        form_add_class = Add_class()
        if form_add_class.validate_on_submit():
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            if db_sess.query(User).\
                    filter(User.grade_for_teacher == form_add_class.add_class.data).first():
                user.classes = user.classes + ';' + form_add_class.add_class.data
                db_sess.add(user)
                db_sess.commit()
                return redirect('/main_page')
            else:
                message = 'Такого класса не существует'
    form_name = Edit_name()
    if form_name.validate_on_submit():
        if form_name.name.data.isalpha():
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            user.name = form_name.name.data.capitalize()
            db_sess.add(user)
            db_sess.commit()
            return redirect('/main_page')
        else:
            message = 'Введите настоящее имя'
    form_surname = Edit_surname()
    if form_surname.validate_on_submit():
        if form_surname.surname.data.isalpha():
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            user.surname = form_surname.surname.data.capitalize()
            db_sess.add(user)
            db_sess.commit()
            return redirect('/main_page')
        else:
            message = 'Введите настоящую фамилию'
    if current_user.teacher:
        if not current_user.subject or not current_user.class_num:
            disabled = True
        else:
            disabled = False
    if not current_user.teacher:
        if not current_user.grade:
            disabled = True
        else:
            disabled = False
    return render_template(html, title='Личный кабинет', form=form,
                           surname=current_user.surname, name=current_user.name,
                           grade=grade, grade_id=current_user.grade, form_name=form_name,
                           form_surname=form_surname, form_class=form_class,
                           class_num=current_user.class_num, message=message,
                           grade_for_teacher=current_user.grade_for_teacher,
                           form_add_class=form_add_class, classes=classes, form_subject=form_subject,
                           subject=current_user.subject, disabled=disabled)


def get_classes(url):
    classes = []
    db_sess = db_session.create_session()
    for i in current_user.classes.split(';'):
        class_ = db_sess.query(User). \
            filter(User.grade_for_teacher == i).first()
        classes.append([class_.class_num, f'{url}{class_.grade}'])
    return classes


@app.route('/marks')
@login_required
def marks():
    db_sess = db_session.create_session()
    if current_user.teacher:
        classes = get_classes('marks/table?class_id=')
        return render_template("teacher_marks.html", classes=classes, edit=False)
    else:
        student_marks = db_sess.query(Marks).filter(Marks.user_id == current_user.id)\
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
        return render_template('student_marks.html', dates=dates, dict_marks=dict_marks,
                               title='Оценки')


@app.route('/marks/table')
@login_required
def table_marks():
    if current_user.teacher:
        db_sess = db_session.create_session()
        class_id = request.args.get('class_id')
        students = db_sess.query(User).filter(User.grade == class_id, User.teacher == 0).\
            order_by(User.surname.asc()).all()
        students_id = [i.id for i in students]
        names = [f'{i.name[0]}. {i.surname}' for i in students]
        marks = db_sess.query(Marks).filter(Marks.user_id.in_(students_id),
                                            Marks.teacher_id == current_user.id).\
            order_by(Marks.date.asc()).all()
        marks_dict = {}
        for num, i in enumerate(students):
            for j in marks:
                if j.user_id == i.id:
                    if names[num] in marks_dict:
                        marks_dict[names[num]].append({'date': j.date,
                                                       'mark': j.mark,
                                                       'id': f'table/edit?mark_id={j.id}'})
                    else:
                        marks_dict[names[num]] = [{'date': j.date,
                                                   'mark': j.mark,
                                                   'id': f'table/edit?mark_id={j.id}'}]
        for key, val in marks_dict.items():
            stud_marks = [int(j['mark']) for j in val]
            marks_dict[key].append({'sr_ball': sum(stud_marks) / len(stud_marks)})
        d = [i.date for i in marks]
        dates = ['Фамилия']
        for i in d:
            if i not in dates:
                dates.append(i)
        dates.append('Средний балл')
        class_id = 'table/add?class_id=' + class_id
        return render_template('teacher_marks.html', edit=True, marks=marks_dict,
                               dates=dates, class_id=class_id,
                               title='Оценки')


@app.route('/marks/table/edit', methods=['GET', 'POST'])
@login_required
def edit_marks():
    mark_id = request.args.get('mark_id')
    db_sess = db_session.create_session()
    mark = db_sess.query(Marks).filter(Marks.id == mark_id).first()
    student = db_sess.query(User).filter(User.id == mark.user_id).first()
    form_edit = Edit_mark()
    if form_edit.validate_on_submit():
        if 1 < form_edit.mark.data < 6:
            mark.mark = form_edit.mark.data
            db_sess.add(mark)
            db_sess.commit()
            return redirect('/marks')
    form_delete = Delete_mark()
    if form_delete.validate_on_submit():
        db_sess.delete(mark)
        db_sess.commit()
        return redirect('/marks')
    return render_template('edit_mark.html', surname=student.surname, date=mark.date,
                           form_edit=form_edit, form_delete=form_delete, title='Редактирование оценок')


@app.route('/homework')
@login_required
def homework():
    db_sess = db_session.create_session()
    if current_user.teacher:
        classes = get_classes('homework/table?class_id=')
        return render_template('teacher_homework.html', classes=classes, table=True)
    else:
        homeworks = db_sess.query(Exercises).\
                        filter(Exercises.class_id == current_user.grade).\
                        order_by(Exercises.date).all()
        hw_list = []
        for i in homeworks:
            subject = db_sess.query(User).filter(User.id == i.teacher_id, User.teacher).first().subject
            hw_list.append({'date': i.date, 'text': i.homework, 'subject': subject})
        return render_template('student_homework.html', hw_list=hw_list, table=True, title='Домашние работы')


@app.route('/homework/table')
@login_required
def table_homework():
    if current_user.teacher:
        class_id = request.args.get('class_id')
        db_sess = db_session.create_session()
        homeworks = db_sess.query(Exercises).\
            filter(Exercises.teacher_id == current_user.id, Exercises.class_id == class_id).\
            order_by(Exercises.date.desc()).all()
        homeworks_dict = []
        for i in homeworks:
            homeworks_dict.append({'date': i.date,
                                   'href': f'/homework/table/edit?homework_id={i.id}',
                                   'text': i.homework})
        class_id = '/homework/table/add?class_id=' + class_id
        return render_template('teacher_homework.html', table=False,
                               homeworks_dict=homeworks_dict, class_id=class_id, title='Домашние работы')


@app.route('/homework/table/edit', methods=['GET', 'POST'])
@login_required
def edit_homework():
    if current_user.teacher:
        homework_id = request.args.get('homework_id')
        db_sess = db_session.create_session()
        form = Edit_homework()
        if form.validate_on_submit():
            task = db_sess.query(Exercises).filter(Exercises.id == homework_id).first()
            class_id = f'/homework/table?class_id={task.class_id}'
            task.homework = form.text.data
            db_sess.add(task)
            db_sess.commit()
            return redirect(class_id)
        return render_template('edit_homework.html', form=form, title='Редактирование домашней работы')


@app.route('/tests')
@login_required
def tests():
    db_sess = db_session.create_session()
    if current_user.teacher:
        classes = get_classes('tests/table?class_id=')
        return render_template('teacher_tests.html', classes=classes, choice=True, title='Выбор класса')
    else:
        id = str(current_user.id)
        stud_tests = db_sess.query(Tests).\
            filter(Tests.class_id == current_user.grade).all()
        tests = []
        for i in stud_tests:
            if not(i.students) or str(current_user.id) not in i.students.split(';'):
                tests.append({'subject': i.subject,
                              'href': f'/tests/pass?test_id={i.id}&subject={i.subject}',
                              'name': i.name})
        return render_template('choice_test.html', title="Доступные тесты", tests=tests)


@app.route('/tests/pass', methods=['GET', 'POST'])
@login_required
def pass_test():
    if not current_user.teacher:
        db_sess = db_session.create_session()
        test_id = request.args.get('test_id')
        subject = request.args.get('subject')
        if request.method == 'GET':
            questions = db_sess.query(Question).filter(Question.id_test == test_id).all()
            questions_list = []
            global ides
            ides = []
            for i in questions:
                questions_list.append({'question': i.question, 'answers': i.answer_options.split('&'), 'id': i.id})
                ides.append(i.id)
            return render_template('test.html', questions_list=questions_list, subject=subject, title='Тест')
        elif request.method == 'POST':
            true_answers = 0
            for i in ides:
                correct_answer = db_sess.query(Question).filter(Question.id == i).first().correct_answer
                if request.form[f'answer={i}'] == correct_answer:
                    true_answers += 1
            percent = 100 / len(ides) * true_answers
            if percent >= 85:
                mark1 = 5
            elif 70 <= percent < 85:
                mark1 = 4
            elif 50 <= percent < 70:
                mark1 = 3
            elif percent < 50:
                mark1 = 2
            test = db_sess.query(Tests).filter(Tests.id == test_id).first()
            if test.students:
                test.students = test.students + str(current_user.id) + ';'
            else:
                test.students = str(current_user.id) + ';'
            mark = Marks()
            mark.teacher_id = test.teacher_id
            mark.user_id = current_user.id
            mark.mark = mark1
            x = db_sess.query(Marks).filter(Marks.date == datetime.date.today(),
                                            Marks.teacher_id == test.teacher_id,
                                            Marks.user_id == current_user.id).first()
            if x:
                db_sess.delete(x)
            db_sess.add(mark)
            db_sess.add(test)
            db_sess.commit()
            return redirect('/main_page')


@app.route('/tests/table', methods=['GET', 'POST'])
def create_new_test():
    db_sess = db_session.create_session()
    if current_user.teacher:
        class_id = request.args.get('class_id')
        form = Create_test()
        if form.validate_on_submit():
            kolvo = form.kolvo.data
            name = form.name.data
            test = Tests()
            x = db_sess.query(Tests).filter(Tests.class_id == class_id, Tests.name == name).first()
            if x:
                db_sess.delete(x)
                db_sess.commit()
            test.name = name
            test.teacher_id = current_user.id
            test.class_id = class_id
            test.subject = current_user.subject
            db_sess.add(test)
            db_sess.commit()
            test_id = db_sess.query(Tests).filter(Tests.class_id == class_id, Tests.name == name).first().id
            return redirect(f'/tests/table/create?class_id={class_id}&kolvo={kolvo}&test_id={test_id}')
        return render_template('teacher_tests.html', choice=False, form=form, title='Тест')


@app.route('/tests/table/create', methods=['GET', 'POST'])
@login_required
def create_test():
    if current_user.teacher:
        class_id = request.args.get('class_id')
        kolvo = request.args.get('kolvo')
        test_id = request.args.get('test_id')
        db_sess = db_session.create_session()
        if request.method == 'GET':
            return render_template('create_test.html', kolvo=int(kolvo), title='Создание теста')
        elif request.method == 'POST':
            for i in range(int(kolvo)):
                question = Question()
                question.question = request.form[f'question={i}']
                question.correct_answer = request.form[f'true_answer={i}']
                question.id_test = test_id
                question.subject = current_user.subject
                x = [request.form[f'answer2={i}'], request.form[f'answer3={i}'],
                     request.form[f'answer4={i}'], request.form[f'true_answer={i}']]
                shuffle(x)
                question.answer_options = '&'.join(x)
                db_sess.add(question)
                db_sess.commit()
            return redirect('/main_page')


@app.route('/homework/table/add', methods=['GET', 'POST'])
@login_required
def add_homework():
    if current_user.teacher:
        class_id = request.args.get('class_id')
        db_sess = db_session.create_session()
        form = Add_homework()
        if form.validate_on_submit():
            exercise = Exercises()
            exercise.homework = form.text.data
            exercise.class_id = class_id
            exercise.teacher_id = current_user.id
            date = form.date.data
            ex = db_sess.query(Exercises).filter(Exercises.date == date).first()
            if ex:
                db_sess.delete(ex)
            exercise.date = date
            if db_sess.query(User).filter(User.grade == class_id).first():
                db_sess.add(exercise)
                db_sess.commit()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return redirect(f'https://test.magnumopusproject.xyz/homework/table?class_id={class_id}')
        return render_template('add_homework.html', form=form, title='Добавить домашнюю работу')


@app.route('/marks/table/add', methods=['GET', 'POST'])
@login_required
def add_mark():
    if current_user.teacher:
        db_sess = db_session.create_session()
        class_id = request.args.get('class_id')
        students = db_sess.query(User).filter(User.grade == class_id, User.teacher == 0). \
            order_by(User.surname.asc()).all()
        surnames = [i.surname for i in students]
        if request.method == 'GET':
            return render_template('add_marks.html', surnames=surnames, title='Поставить оценку')
        elif request.method == 'POST':
                date = request.form['date']
                date = datetime.date(*[int(i) for i in date.split('-')])
                for i in surnames:
                    student = db_sess.query(User).filter(User.surname == i, User.grade == class_id).first()
                    students_marks = db_sess.query(Marks).\
                        filter(Marks.user_id == student.id, Marks.date == date).first()
                    if students_marks and request.form[i]:
                        db_sess.delete(students_marks)
                        db_sess.commit()
                    mark = Marks()
                    mark.user_id = int(student.id)
                    mark.teacher_id = int(current_user.id)
                    mark.date = date
                    if request.form[i]:
                        mark.mark = int(request.form[i])
                        db_sess.add(mark)
                        db_sess.commit()
                return redirect(f'/marks/table?class_id={class_id}')



@app.route('/reg')
@login_required
def user_id():
    uid = request.args.get('user_id')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == current_user.login).first()
    user.vk_id = uid
    db_sess.add(user)
    db_sess.commit()
    vk_session = vk_api.VkApi(
        token=open('data/token.txt', mode='r').read())
    vk = vk_session.get_api()
    vk.messages.send(user_id=uid,
                     message="Вы разрешили отправку вам сообщений",
                     random_id=randint(0, 2 ** 64))
    vk.messages.send(user_id=uid,
                     message="Чтобы получить дз напишите: 'дай дз'",
                     random_id=randint(0, 2 ** 64))
    return redirect('/main_page')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/schools.db")
    app.run(host='127.0.0.1', port=5000)
    # serve(app, host='0.0.0.0', port=5000)

