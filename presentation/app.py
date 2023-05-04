# todo: сделать вывод flash-сообщений,
#  методы логического слоя теперь возвращают кортеж
#  ("сообщение, "тип") вывод никак не организован


import time
from os import sys
sys.path.append("C:\\Users\\anari\\WebstormProjects\\Play-n-study-backend")
import flask_admin
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, flash, make_response, url_for
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from presentation.UserLogin import UserLogin
from logic.facade import LogicFacade
from data.types import User
from flask_admin.contrib.sqla import ModelView
from data.models import *


class UserMV(ModelView):
    excluded_list_columns = ('password', 'avatar')
    list_columns = ('user_id', 'username', 'email', 'city')


class CuratorMV(ModelView):
    list_columns = ('cur_rel_id', 'user_id', 'course_id')


class CoursesMV(ModelView):
    list_columns = ('course_id', 'name')



engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.secret_key = 'super secret key'

login_manager = LoginManager(app)

admin = flask_admin.Admin(app, name='Admin Panel')
admin.add_view(UserMV(UsersModel, session))
admin.add_view(CuratorMV(CuratorsModel, session))
admin.add_view(CoursesMV(CoursesModel, session))


# logic layer instance
logic = LogicFacade(session)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().from_db(logic, user_id)


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
        user = logic.user_auth(request.form['email'], request.form['password'])
        if user is None:
            flash('Неверный логин/пароль', 'error')
            return render_template('login.html')
        user_login = UserLogin().create(user)
        login_user(user_login)
        return redirect(f"/profiles/{user.user_id}")
    return render_template('login.html')


@app.route("/registration", methods=["POST", "GET"])
def handle_register():
    if request.method == 'POST':
        response = logic.user_register(request.form.copy())
        flash(*response)
    return render_template("registration.html")


@app.route('/index')
@app.route('/me')
@login_required
def handle_me():
    user_id = current_user.get_id()
    user = logic.get_user_for_profile(user_id)
    return render_template('profile.html', user=user, is_me=True, need_subscribe=False)

@app.route('/tests')
def handle_tests():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('tests.html', user=user)

@app.route('/')
def handle_task():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('tasks.html', user=user)


@app.route('/about')
def about():
    return "About"


@app.route('/courses/<int:user_id>')
def handle_courses(user_id):
    user = logic.get_user_by_id(user_id)
    return render_template("courses.html", user=user)

@app.route('/test_preview')
def handle_test_preview():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template("test_preview.html", user=user)

@app.route('/index')
def handle_index():
    user_id = current_user.get_id()
    user = user_repository.get_user_by_id(user_id)
    return render_template("index1.html", user=user)

@app.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    user = logic.get_user_for_profile(user_id, current_user.get_id())
    return render_template("profile.html", user=user,
                           need_subscribe=user.need_subscribe, is_me=user.is_me)


@app.route('/subscriptions/<int:user_id>', methods=["POST", "GET"])
def handle_subscriptions(user_id):
    if request.method == "GET":
        user = logic.get_user_for_profile(user_id, current_user.get_id())
        return render_template('subscriptions.html', user=user, user_id=user_id)
    elif request.method == "POST":
        query = request.form['query']
        if len(query) > 0:
            found = logic.get_users_by_query(query)
            return render_template("subscriptions.html", user=User(), found=found, user_id=user_id)
    return render_template("subscriptions.html", user=User(), found=None, user_id=user_id)


@app.route('/reviews')
def handle_reviews():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('reviews.html', user=user)


@app.route('/test_constructor', methods=["GET"])
def handle_test_constructor():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('test_constructor.html', user=user)


@app.route('/test_constructor', methods=["POST"])
def handle_result_test():
    response = logic.save_test(request.form)
    if response[1] == 'success':
        return "успешно"
    return "ошибка"


@app.route('/tests/<int:test_id>')
def handle_load_test(test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    total_score = 0
    for question in test.content.questions:
        if question.score:
            total_score += question.score
    return render_template('test.html', user=user, test=test.content, score=total_score, time=time.time())


@app.route('/tests_edit/<int:test_id>')
def handle_edit_test(test_id):
    test = logic.get_test_by_id(test_id=test_id)
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('test_editor.html', user=user, test=test.content)


@app.route('/tests_edit/<int:test_id>', methods=["POST"])
def handle_edit_test_save(test_id):
    response = logic.edit_test(request.form.to_dict())
    if response[1] == 'success':
        return "успешно"
    return "ошибка"


@app.route('/tests/<int:test_id>', methods=["POST"])
def handle_check_test(test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    result = logic.get_test_result(test, request.form)

    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_result.html', user=user, test=test.content, score=result.total_score, total_score=result.total_current_score, result=result.result, total_time=result.total_time)


@app.route('/save_test', methods=["POST"])
def handle_save_test():
    pass


# route for debug
# @app.route('/debug')
# def handle_debug():
# pass


@app.route('/achievements/<int:user_id>')
def handle_achievements(user_id):
    # todo: сделать ачивки пользователя
    pass


@app.route('/course')
def handle_course():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('course.html', user=user)


@app.route('/information')
def handle_information():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('information.html', user=user)


@app.route('/changecity', methods=['POST'])
def handle_change_user_data():
    response = logic.change_user_data(request.form, current_user.get_id())
    return redirect(url_for('handle_settings'))


@app.route('/settings', methods=["GET"])
def handle_settings():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('settings.html', user=user)


@app.route('/uploadava', methods=["POST", "GET"])
@login_required
def handle_upload():
    if request.method == 'POST':
        logic.user_avatar_upload(request.files['file'], current_user)
    return redirect(url_for('handle_settings'))


@app.route('/userava/<int:user_id>')
@login_required
def handle_userava(user_id):
    img = logic.get_avatar(app, user_id)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/subscribe/<int:user_id>')
@login_required
def handle_subscribe(user_id):
    response = logic.add_sub_relation(user_id, current_user.get_id())
    if response:
        return redirect(f"/profiles/{user_id}")
    else:
        flash('Ошибка при подписке', 'error')


@app.route('/unsubscribe/<int:user_id>')
@login_required
def handle_unsubscribe(user_id):
    response = logic.remove_sub_relation(user_id, current_user.get_id())
    if response:
        return redirect(f"/profiles/{user_id}")
    else:
        flash('Ошибка при отписке', 'error')


if __name__ == "__main__":
    app.run(debug=True)
