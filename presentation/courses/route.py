from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.types import User
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
@courses_bp.route('/test_preview/<int:test_id>')
def handle_test_preview(test_id):
    test = logic.get_test_by_id(test_id)
    user_id = current_user.get_id()
    course = logic.get_course(test.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    return render_template("test_preview.html", user=user, test=test, course=course)


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


@courses_bp.route('/course_constructor', methods=['GET'])
@login_required
def handle_course_constructor():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('course_constructor.html', user=user)


@login_required
@courses_bp.route('/create_course/<int:user_id>', methods=['POST'])
def handle_course_create(user_id):
    course_name = request.form['courseName']
    course_desc = request.form['description']
    course_cat = request.form['category']
    logic.add_course(course_name, course_desc, course_cat)
    user = logic.get_user_for_courses(user_id)
    return render_template("courses.html", user=user, found=None, user_id=user_id)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["POST"])
def handle_result_test(course_id, unit_id):
    response = logic.save_test(request.form, course_id, unit_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>')
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


@courses_bp.route('/course_preview/<int:course_id>')
@login_required
def handle_course(course_id):
    course = logic.course_get_for_preview(course_id, current_user.get_id())
    return render_template('course.html', course=course)

