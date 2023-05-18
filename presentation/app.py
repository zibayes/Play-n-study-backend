# todo: сделать вывод flash-сообщений,
#  методы логического слоя теперь возвращают кортеж
#  ("сообщение, "тип") вывод никак не организован
import json
# todo: убрать все модели users там где это не надо, заменить на current_user
#  в самом шаблоне

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
from data.types import User, Progress, TestContent
from logic.test import TestResult


engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.secret_key = 'super secret key'

login_manager = LoginManager(app)

# logic layer instance
logic = LogicFacade(session)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().from_db(logic, user_id)


# @app.route('/admin')
# @login_required
# def handle_admin():
#     is_admin = logic.is_user_admin(current_user.get_id())
#     if not is_admin:
#         return "not allowed"
#     return render_template()


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('index.html')


@app.route('/debug')
def debug_route():
    if logic.is_user_admin(current_user.get_id()):
        return "admin"
    return "not admin"


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


@login_required
@app.route('/course/<int:course_id>')
def handle_tests(course_id):
    course = logic.get_course(course_id, current_user.get_id())
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    print(course.content['body'])
    for unit in course.content['body']:
        for test in unit['tests']:
            test["test"] = logic.get_test_by_id(test["test_id"])
    if course is None:
        return render_template('index.html', user=user)
    return render_template('tests.html', user=user, course=course)


@app.route('/')
def handle_task():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('tasks.html', user=user)


@app.route('/about')
def about():
    return "About"


@login_required
@app.route('/courses/<int:user_id>', methods=['POST', 'GET'])
def handle_courses(user_id):
    match request.method:
        case 'GET':
            user = logic.get_user_for_courses(user_id)
            return render_template("courses.html", user=user, found=None, user_id=user_id)
        case 'POST':
            query = request.form['query']
            if len(query) > 0:
                found = logic.courses_get_by_query(query)
                return render_template("courses.html", found=found, user=User(), user_id=user_id)


@app.route('/courseava/<int:course_id>')
@login_required
def handle_course_ava(course_id):
    img = logic.course_get_avatar(app, course_id)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@login_required
@app.route('/course/<int:course_id>/test_preview/<int:test_id>')
def handle_test_preview(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user_id = current_user.get_id()
    course = logic.get_course(test.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    progress = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    to_delete = []
    # progress[i].progress = Progress.from_json(json.loads(str(progress[i].progress).replace("'", '"')))
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != test_id:
            to_delete.append(i)

    for i in reversed(to_delete):
        progress.pop(i)


    # print(progress[0].progress)
    return render_template("test_preview.html", user=user, test=test, course=course, progresses=progress)


@login_required
@app.route('/delete_test/<int:course_id>/<int:test_id>', methods=['POST'])
def handle_delete_test(course_id, test_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    index_to_delete = 0
    inner_index_to_delete = 0
    is_break = False
    for unit in course.content['body']:
        for test in unit['tests']:
            if int(test['test_id']) == test_id:
                is_break = True
                break
            inner_index_to_delete += 1
        if is_break:
            break
        inner_index_to_delete = 0
        index_to_delete += 1
    logic.update_course(course)
    logic.remove_test(test_id)
    return redirect(f'/course_editor/{course_id}')


@login_required
@app.route('/delete_unit/<int:course_id>/<int:unit_id>', methods=['POST'])
def handle_delete_unit(course_id, unit_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    index_to_delete = 0
    for unit in course.content['body']:
        if int(unit['unit_id']) == unit_id:
            break
        index_to_delete += 1

    for test in course.content['body'][index_to_delete]['tests']:
        logic.remove_test(test['test_id'])
    course.content['body'].pop(index_to_delete)
    logic.update_course(course)
    return redirect(f'/course_editor/{course_id}')


@login_required
@app.route('/delete_course/<int:course_id>', methods=['POST'])
def handle_delete_course(course_id):
    user_id = current_user.get_id()
    course = logic.get_course_without_rel(course_id)
    for unit in course.content['body']:
        for test in unit['tests']:
            logic.remove_test(test['test_id'])
    rels = logic.get_course_rels_all(course_id)
    if rels:
        for rel in rels:
            logic.rel_remove_course_rel(rel.cour_rel_id)
    # logic.course_leave(course.course_id, user_id)
    logic.remove_course(course.course_id)
    return redirect(f'/courses/{user_id}')


@login_required
@app.route('/course_editor/<int:course_id>', methods=['GET'])
def handle_course_editor(course_id):
    course = logic.get_course(course_id, current_user.get_id())
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    for unit in course.content['body']:
        for test in unit['tests']:
            test["test"] = logic.get_test_by_id(test["test_id"])
    if course is None:
        return render_template('index.html', user=user)
    return render_template('course_editor.html', user=user, course=course)


@login_required
@app.route('/course_editor/<int:course_id>', methods=['POST'])
def handle_course_editor_save_unit(course_id):
    unit_name = request.form['newUnitName']
    logic.update_course_add_unit(course_id, unit_name)
    return redirect(f'/course_editor/{course_id}')


@login_required
@app.route('/create_course/<int:user_id>', methods=['POST'])
def handle_course_create(user_id):
    print(request.files)
    print(request.form)
    course_name = request.form['courseName']
    course_desc = request.form['description']
    course_cat = request.form['category']
    if request.files:
        course_ava = request.files['file']
    else:
        course_ava = None
    logic.add_course(course_name, course_desc, course_cat, course_ava, current_user)
    user = logic.get_user_for_courses(user_id)
    return render_template("courses.html", user=user, found=None, user_id=user_id)


@login_required
@app.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    user = logic.get_user_for_profile(user_id, current_user.get_id())
    return render_template("profile.html", user=user,
                           need_subscribe=user.need_subscribe, is_me=user.is_me)


@login_required
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


@login_required
@app.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["GET"])
def handle_test_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('test_constructor.html', user=user, course_id=course_id, unit_id=unit_id)


@login_required
@app.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["POST"])
def handle_result_test(course_id, unit_id):
    response = logic.save_test(request.form, course_id, unit_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@app.route('/course/<int:course_id>/tests/<int:test_id>', methods=["GET"])
def handle_load_test(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    total_score = 0
    for question in test.content.questions:
        if question.score:
            total_score += question.score
    return render_template('test.html', user=user, test=test.content, score=total_score, time=time.time())


@login_required
@app.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>')
def handle_edit_test(course_id, test_id):
    test = logic.get_test_by_id(test_id=test_id)
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('test_editor.html', user=user, test=test.content)


@login_required
@app.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["POST"])
def handle_edit_test_save(course_id, test_id):
    response = logic.edit_test(request.form, test_id, course_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@app.route('/course/<int:course_id>/tests/<int:test_id>', methods=["POST"])
def handle_check_test(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    result = logic.get_test_result(test, request.form)
    progress = Progress(progress_id=None, completed=True, type='test',
                        content=test.content.toJSON(), test_id=test_id, result=result.to_json())
    logic.add_progress(course_id=course_id, user_id=user.user_id, progress=Progress.to_json(progress))
    print(test.content.toJSON())

    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_result.html', user=user, test=test.content, score=result.total_score,
                           total_score=result.total_current_score, result=result.result, total_time=result.total_time)


@login_required
@app.route('/course/<int:course_id>/test_result/<int:test_id>/<int:progress_id>', methods=["POST"])
def handle_show_test_result(course_id, test_id, progress_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    progress = logic.get_progress_by_id(progress_id)
    progress.progress = Progress.from_json(progress.progress)
    result = TestResult.from_json(json.loads(progress.progress['result']))
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_result.html', user=user, test=TestContent.from_json(progress.progress['content']), score=result.total_score,
                           total_score=result.total_current_score, result=result.result, total_time=result.total_time)


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


@app.route('/course_preview/<int:course_id>')
def handle_course(course_id):
    course = logic.course_get_for_preview(course_id, current_user.get_id())
    return render_template('course.html', course=course)


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
    img = logic.get_user_avatar(app, user_id)
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


@app.route('/api/joincourse/<int:course_id>')
@login_required
def handle_join_course(course_id):
    response = logic.course_join(course_id, current_user.get_id())
    if response:
        return redirect(f'/course_preview/{course_id}')
    flash('Ошибка при подписке', 'error')


@app.route('/api/leavecourse/<int:course_id>')
@login_required
def handle_join_leave_course(course_id):
    response = logic.course_leave(course_id, current_user.get_id())
    if response:
        return redirect(f'/course_preview/{course_id}')
    flash('Ошибка при отписке', 'error')


if __name__ == "__main__":
    app.run(debug=True)
