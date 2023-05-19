import time
import json

from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.types import User, Progress, TestContent, Article
from logic.test import TestResult
from logic.facade import LogicFacade

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)

courses_bp = Blueprint('courses', __name__)


@login_required
@courses_bp.route('/course/<int:course_id>')
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


@login_required
@courses_bp.route('/courses/<int:user_id>', methods=['POST', 'GET'])
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


@login_required
@courses_bp.route('/course/<int:course_id>/test_preview/<int:test_id>')
def handle_test_preview(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user_id = current_user.get_id()
    course = logic.get_course(test.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    progress = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    to_delete = []
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != test_id:
            to_delete.append(i)
    for i in reversed(to_delete):
        progress.pop(i)
    return render_template("test_preview.html", user=user, test=test, course=course, progresses=progress)


@login_required
@courses_bp.route('/delete_test/<int:course_id>/<int:test_id>', methods=['POST'])
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
@courses_bp.route('/delete_unit/<int:course_id>/<int:unit_id>', methods=['POST'])
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
@courses_bp.route('/delete_course/<int:course_id>', methods=['POST'])
def handle_delete_course(course_id):
    user_id = current_user.get_id()
    course = logic.get_course_without_rel(course_id)
    for unit in course.content['body']:
        for test in unit['tests']:
            logic.remove_test(test['test_id'])
    logic.course_leave(course.course_id, user_id)
    logic.remove_course(course.course_id)
    return redirect(f'/courses/{user_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>', methods=['GET'])
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
@courses_bp.route('/course_editor/<int:course_id>', methods=['POST'])
def handle_course_editor_save_unit(course_id):
    unit_name = request.form['newUnitName']
    logic.update_course_add_unit(course_id, unit_name)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/create_course/<int:user_id>', methods=['POST'])
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
@courses_bp.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["GET"])
def handle_test_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('test_constructor.html', user=user, course_id=course_id, unit_id=unit_id)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["POST"])
def handle_result_test(course_id, unit_id):
    response = logic.save_test(request.form, course_id, unit_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_constructor/<int:unit_id>', methods=["GET"])
def handle_article_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('article_constructor.html', user=user, course_id=course_id, unit_id=unit_id)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_constructor/<int:unit_id>', methods=["POST"])
def handle_article_save(course_id, unit_id):
    article_text = request.form['Article']
    article = Article(article_id=None, course_id=course_id, content=article_text)
    response = logic.article_add_article(article, course_id, unit_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/create_task/<int:unit_id>', methods=["POST"])
def handle_create_task(course_id, unit_id):
    task_type = request.form['TaskType']
    if task_type == 'test':
        return redirect(url_for('courses.handle_test_constructor', course_id=course_id, unit_id=unit_id))
    else:
        return redirect(url_for('courses.handle_article_constructor', course_id=course_id, unit_id=unit_id))


@login_required
@courses_bp.route('/course/<int:course_id>/tests/<int:test_id>', methods=["GET"])
def handle_load_test(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    total_score = 0
    for question in test.content.questions:
        if question.score:
            total_score += question.score
    return render_template('test.html', user=user, test=test.content, score=total_score, time=time.time())


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["GET"])
def handle_edit_test(course_id, test_id):
    test = logic.get_test_by_id(test_id=test_id)
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('test_editor.html', user=user, test=test.content)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["POST"])
def handle_edit_test_save(course_id, test_id):
    response = logic.edit_test(request.form, test_id, course_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/tests/<int:test_id>', methods=["POST"])
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
@courses_bp.route('/course/<int:course_id>/test_result/<int:test_id>/<int:progress_id>', methods=["POST"])
def handle_show_test_result(course_id, test_id, progress_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    progress = logic.get_progress_by_id(progress_id)
    progress.progress = Progress.from_json(progress.progress)
    result = TestResult.from_json(json.loads(progress.progress['result']))
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_result.html', user=user, test=TestContent.from_json(progress.progress['content']), score=result.total_score,
                           total_score=result.total_current_score, result=result.result, total_time=result.total_time)


@courses_bp.route('/course_preview/<int:course_id>')
@login_required
def handle_course(course_id):
    course = logic.course_get_for_preview(course_id, current_user.get_id())
    return render_template('course.html', course=course)

