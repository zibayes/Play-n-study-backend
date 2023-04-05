import copy
import sys

sys.path.append("C:\\Users\\anari\\WebstormProjects\\Play-n-study-backend")

from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from infrastructure.auth.UserLogin import UserLogin
from infrastructure.auth.service import get_register_wrong_field_msg
from infrastructure.changes.settings_service import get_wrong_field_msg
from infrastructure.QueryManager import *
from infrastructure.repository.AchievementRepository import AchievementRepository
from infrastructure.repository.UserRepository import UserRepository
from infrastructure.repository.AchieveRelRepository import AchieveRelRepository
from domain.User import User

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

print(session)

app = Flask(__name__)
app.secret_key = 'super secret key'
login_manager = LoginManager(app)

# Repositories
user_repository = UserRepository(session)
achieve_rel_repository = AchieveRelRepository(session)
achievement_repository = AchievementRepository(session)
course_repository = CourseRepository(session)
course_rel_repository = CourseRelRepository(session)
curator_repository = CuratorRepository(session)
review_repository = ReviewRepository(session)
task_repository = TaskRepository(session)
sub_rel_repository = SubRelRepository(session)

# QueryManager
query_manager = QueryManager(user_repository=user_repository,
                             achievement_repository=achievement_repository,
                             achieve_rel_repository=achieve_rel_repository,
                             course_repository=course_repository,
                             course_rel_repository=course_rel_repository,
                             curator_repository=curator_repository,
                             review_repository=review_repository,
                             task_repository=task_repository,
                             sub_rel_repository=sub_rel_repository)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().from_db(user_repository, user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('index.html')


@app.route("/logout")
@login_required
def handle_logout():
    logout_user()
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        user = user_repository.get_user_by_email(request.form['email'])
        if user is None:
            user = user_repository.get_user_by_username(request.form['email'])

        if user is not None and check_password_hash(user.password, request.form['password']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('handle_me'))
        flash('Неверный логин/пароль', 'error')

    return render_template('login.html')


@app.route("/registration", methods=["POST", "GET"])
def handle_register():
    # Ссылки для перенаправления в случае неудачной/удачной регистрации
    current_template = url_for('handle_register').replace('/', '') + '.html'
    login_url = url_for('handle_login')

    form_data = request.form.copy()
    if request.method == 'POST':
        # Получаем либо сообщение об ошибке, либо None если все ОК
        error = get_register_wrong_field_msg(user_repository, form_data)
        if error is None:

            user = User(user_id=None,
                        email=request.form.get('email'),
                        username=request.form.get('username'),
                        city='',
                        avatar='',
                        password=generate_password_hash(request.form.get('password'))
                        )
            if user_repository.add_user(user):
                flash('Вы успешно зарегистрированы', 'success')
                return redirect(login_url)
            flash('Ошибка при add_user', 'error')
        else:
            flash(error, 'error')
    return render_template(current_template)


@app.route('/')
@app.route('/index')
@app.route('/me')
@login_required
def handle_me():
    # current_user.achievements = query_manager.get_user_achievements(current_user.id)
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    user.achievements = query_manager.get_user_achievements(user_id)
    user.courses = query_manager.get_user_courses(user_id)

    user.subs = query_manager.get_user_subs(user.user_id)
    user.subs_count = len(user.subs) if user.subs else 0
    user.sub_to = query_manager.get_user_sub_to(user.user_id)
    user.sub_to_count = len(user.sub_to) if user.sub_to else 0

    return render_template('profile.html', user=user)


@app.route('/about')
def about():
    return "About"


@app.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    user = user_repository.get_user_by_id(user_id)
    user.achievements = query_manager.get_user_achievements(user.user_id)
    user.courses = query_manager.get_user_courses(user.user_id)
    user.subs = query_manager.get_user_subs(user.user_id)
    user.subs_count = len(user.subs) if user.subs else 0
    user.sub_to = query_manager.get_user_sub_to(user.user_id)
    user.sub_to_count = len(user.sub_to) if user.sub_to else 0
    return render_template("profile.html", user=user)


#
# @app.route('/friends')
# def handle_friends():
#     return render_template('subscriptions.html')


@app.route('/subscriptions/<int:user_id>', methods=["POST", "GET"])
def handle_subscriptions(user_id):
    if request.method == "GET":
        user = user_repository.get_user_by_id(user_id)
        user.sub_to = query_manager.get_user_sub_to(user.user_id)
        return render_template('subscriptions.html', user=user, user_id=user_id)

    user = User(None, None, None, None, None, None)
    query = request.form['query']
    if len(query) > 0:
        found = query_manager.get_users_by_query(query)
        return render_template("subscriptions.html", user=user, found=found, user_id=user_id)
    return render_template("subscriptions.html", user=user, found=None, user_id=user_id)

@app.route('/task')
def handle_task():
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    return render_template('tasks.html', user=user)

@app.route('/reviews')
def handle_reviews():
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    return render_template('reviews.html', user=user)


@app.route('/test_constructor', methods=["GET"])
def handle_test_constructor():
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    return render_template('test_constructor.html', user=user)


@app.route('/test_constructor', methods=["POST"])
def handle_result_test():
    test_form = request.form.to_dict()
    test_name = test_form.pop("testName")
    questions_count = 0
    for key in test_form.keys():
        if "Question-" in key:
            questions_count += 1
    question_type = ""
    test = []
    questions = {}
    for i in range(questions_count):
        for key, value in test_form.items():
            if "QuestionType-" in key:
                question_type = value
                break
        question = ""
        new_form = copy.deepcopy(test_form)
        if question_type in ("Единственный ответ", "Множественный ответ"):
            is_right_answer = False
            for key, value in test_form.items():
                if "Question-" in key:
                    questions[value] = []
                    question = value
                if "Answer-" in key and "Right_Answer-" not in key:
                    questions[question].append({value: is_right_answer})
                    is_right_answer = False
                if "Right_Answer-" in key:
                    is_right_answer = True
                if "QuestionType-" in key:
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question_type == "Краткий свободный ответ":
            for key, value in test_form.items():
                if "Question-" in key:
                    questions[value] = []
                    question = value
                if "Answer-" in key and "Right_Answer-" not in key:
                    questions[question].append(value)
                if "QuestionType-" in key:
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question_type in ("Свободный ответ", "Информационный блок"):
            for key, value in test_form.items():
                if "Question-" in key:
                    questions[value] = False
                if "QuestionType-" in key:
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        test.append((questions, question_type))
        questions = {}
    print(test)
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    return render_template('test.html', user=user, test_name=test_name, test=test)
    # redirect(url_for('handle_settings'))


class Bunch(dict):
    __getattr__, __setattr__ = dict.get, dict.__setitem__


@app.route('/achievements/<int:user_id>')
def handle_achievements(user_id):
    achievements = []
    achievement1 = Bunch()
    achievement1.name = "Отличник"
    achievement1.condition = "Пройдите все тесты на отличную оценку"
    achievement1.image = "static/img/otlychnik.png"
    achievements.append(achievement1)
    achievement2 = Bunch()
    achievement2.name = "Сама скорость"
    achievement2.condition = "Пройдите все тесты на время, не дожидаясь конца таймера"
    achievement2.image = "static/img/speed.jpg"
    achievements.append(achievement2)
    achievement3 = Bunch()
    achievement3.name = "Идеал"
    achievement3.condition = "Пройдите все тесты на максимальный балл"
    achievement3.image = "static/img/ideal.jpg"
    achievements.append(achievement3)
    user = user_repository.get_user_by_id(user_id)
    return render_template("achievements.html", user=user, achievements=achievements)


@app.route('/information')
def handle_information():
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    return render_template('information.html', user=user)


@app.route('/changecity', methods=['POST'])
def handle_changepassword():
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)

    username = user_repository.get_user_by_username(request.form.get('username'))
    if username is not None and username.user_id != user.user_id:
        flash("Такое имя уже занято")
    else:
        user.username = request.form.get('username')

    email = user_repository.get_user_by_email(request.form.get('email'))
    if email is not None and email.user_id != user.user_id:
        flash("Такой email уже занят")
    else:
        user.email = request.form.get('email')

    user.city = request.form.get('city')
    if user_repository.update_user(user):
        flash("Успешно обновлено")
    else:
        flash("Что-то пошло не так")
    return redirect(url_for('handle_settings'))


@app.route('/settings', methods=["POST", "GET"])
def handle_settings():
    user_id = current_user.get_id()
    if request.method == 'POST':
        # need imlement
        return redirect(url_for('handle_settings'))
    else:
        user = user_repository.get_user_by_id(user_id)
        user.achievements = query_manager.get_user_achievements(user_id)
        user.courses = query_manager.get_user_courses(user_id)
        return render_template('settings.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
