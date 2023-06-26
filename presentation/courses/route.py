import copy
import random
import time
import json

from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.types import User, Progress, TestContent, Test, Article
from logic.test import TestResult
from logic.facade import LogicFacade
from markdown import markdown
from access import check_curator_access, check_subscriber_access

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
@check_subscriber_access(current_user)
def handle_tests(course_id):
    course = logic.get_course(course_id, current_user.get_id())
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    results = {}
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.unit_type == 'test':
                test.test = logic.get_test_by_id(test.test_id)
            else:
                test.test = Test(test.test_id, course_id, TestContent(test.article_name, None))
            for progress in progresses:
                if progress.progress['test_id'] == test.test_id and progress.progress['type'] == test.unit_type:
                    results[str(test.test_id) + test.unit_type] = progress.progress['completed']
    if course is None:
        return render_template('index.html', user=user)
    return render_template('tests.html', user=user, course=course, results=results)


@login_required
@courses_bp.route('/course/<int:course_id>/summary')
@check_subscriber_access(current_user)
def handle_course_summary(course_id):
    course = logic.get_course(course_id, current_user.get_id())
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    if course is None:
        return render_template('index.html', user=user)
    progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    results = {}
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.unit_type == 'test':
                test.test = logic.get_test_by_id(test.test_id)
            else:
                test.test = Test(test.test_id, course_id, TestContent(test.article_name, None))
            for progress in progresses:
                if progress.progress['test_id'] == test.test_id and progress.progress['type'] == test.unit_type:
                    results[str(test.test_id) + test.unit_type] = progress.progress['completed']

    marks = {}
    max_marks = {}
    for progress in progresses:
        if progress.progress['result']:
            progress.progress['result'] = TestResult.from_json(json.loads(progress.progress['result']))
            if (str(progress.progress['test_id'])+progress.progress['type']) not in marks.keys():
                marks[str(progress.progress['test_id']) + progress.progress['type']] = []
                max_marks[str(progress.progress['test_id']) + progress.progress['type']] = progress.progress['result'].total_score
            marks[str(progress.progress['test_id'])+progress.progress['type']].append(progress.progress['result'].total_current_score)
    for key in marks.keys():
        marks[key] = max(marks[key])
    total = sum(marks.values())
    total_max = sum(max_marks.values())
    return render_template('course_summary.html', user=user, course=course, results=results,
                           marks=marks, max_marks=max_marks, total=total, total_max=total_max)


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
            else:
                user = logic.get_user_for_courses(user_id)
                return render_template("courses.html", user=user, found=None, user_id=user_id)


@login_required
@courses_bp.route('/course/<int:course_id>/test_preview/<int:test_id>')
@check_subscriber_access(current_user)
def handle_test_preview(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user_id = current_user.get_id()
    course = logic.get_course(test.course_id, user_id)
    user = logic.get_user_by_id(user_id)

    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']

    progress = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    to_delete = []
    max_score = 0
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != test_id:
            to_delete.append(i)
        else:
            progress[i].progress['result'] = TestResult.from_json(json.loads(progress[i].progress['result']))
            if progress[i].progress['result'].total_current_score > max_score:
                max_score = progress[i].progress['result'].total_current_score
    for i in reversed(to_delete):
        progress.pop(i)

    leaders = logic.get_progress_by_course_id_all(course_id)
    leaders_to_show = {}
    leaders_hrefs = {}
    graphic_data = {}
    friends = {}
    subs = logic.get_user_for_subscriptions(user_id).sub_to
    if subs:
        subs = [user.username for user in subs]
    for i in range(len(leaders)):
        if int(leaders[i].progress['test_id']) == test_id:
            leaders[i].progress['result'] = TestResult.from_json(json.loads(leaders[i].progress['result']))
            user_for_table = logic.get_user_by_id(leaders[i].user_id).username
            if user_for_table not in leaders_to_show.keys():
                leaders_to_show[user_for_table] = []
                leaders_hrefs[user_for_table] = leaders[i].user_id
                if subs and user_for_table in subs or user_for_table == user.username:
                    friends[user_for_table] = []
            leaders_to_show[user_for_table].append(leaders[i].progress['result'].total_current_score)
            if subs and user_for_table in subs or user_for_table == user.username:
                friends[user_for_table].append(leaders[i].progress['result'].total_current_score)
    for key in leaders_to_show.keys():
        leaders_to_show[key] = max(leaders_to_show[key])
        if key in friends.keys():
            friends[key] = max(friends[key])
        if leaders_to_show[key] not in graphic_data.keys():
            graphic_data[leaders_to_show[key]] = 0
        graphic_data[leaders_to_show[key]] += 1

    return render_template("test_preview.html", user=user, test=test, course=course, unit_name=unit_name,
                           progresses=progress, max_score=max_score, graphic_data=dict(sorted(graphic_data.items(), key=lambda item: item[0], reverse=False)),
                           leaders=dict(sorted(leaders_to_show.items(), key=lambda item: item[1], reverse=True)), leaders_hrefs=leaders_hrefs, friends=friends)


@login_required
@courses_bp.route('/delete_test/<int:course_id>/<int:test_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_test(course_id, test_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    index_to_delete = 0
    inner_index_to_delete = 0
    is_break = False
    for unit in course.content['body']:
        for test in unit['tests']:
            if int(test.test_id) == test_id:
                is_break = True
                break
            inner_index_to_delete += 1
        if is_break:
            break
        inner_index_to_delete = 0
        index_to_delete += 1
    course.content['body'][index_to_delete]['tests'].pop(inner_index_to_delete)
    logic.update_course(course)
    progresses = logic.get_progress_by_course_id_all(course.course_id)
    for progress in progresses:
        if int(progress.progress['test_id']) == test_id:
            logic.remove_progress(progress.up_id)
    logic.remove_test(test_id)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/delete_article/<int:course_id>/<int:article_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_article(course_id, article_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    index_to_delete = 0
    inner_index_to_delete = 0
    is_break = False
    for unit in course.content['body']:
        for test in unit['tests']:
            if int(test.test_id) == article_id:
                is_break = True
                break
            inner_index_to_delete += 1
        if is_break:
            break
        inner_index_to_delete = 0
        index_to_delete += 1
    course.content['body'][index_to_delete]['tests'].pop(inner_index_to_delete)
    logic.update_course(course)
    progresses = logic.get_progress_by_course_id_all(course.course_id)
    for progress in progresses:
        if int(progress.progress['test_id']) == article_id:
            logic.remove_progress(progress.up_id)
    logic.remove_article(article_id)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/delete_unit/<int:course_id>/<int:unit_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_unit(course_id, unit_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    progresses = logic.get_progress_by_course_id_all(course_id)
    index_to_delete = 0
    for unit in course.content['body']:
        if int(unit['unit_id']) == unit_id:
            break
        index_to_delete += 1

    for test in course.content['body'][index_to_delete]['tests']:
        for progress in progresses:
            if int(progress.progress['test_id']) == test.test_id:
                logic.remove_progress(progress.up_id)
        if test.unit_type == 'test':
            logic.remove_test(test.test_id)
        else:
            logic.remove_article(test.test_id)
    course.content['body'].pop(index_to_delete)
    logic.update_course(course)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/delete_course/<int:course_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_course(course_id):
    user_id = current_user.get_id()
    course = logic.get_course_without_rel(course_id)
    progresses = logic.get_progress_by_course_id_all(course_id)
    for unit in course.content['body']:
        for test in unit['tests']:
            for progress in progresses:
                if int(progress.progress['test_id']) == test.test_id:
                    logic.remove_progress(progress.up_id)
            if test.unit_type == 'test':
                logic.remove_test(test.test_id)
            else:
                logic.remove_article(test.test_id)
    rels = logic.get_course_rels_all(course.course_id)
    for rel in rels:
        logic.course_leave(rel.course_id, rel.user_id)
    curators = logic.get_curators_by_course_id(course_id)
    for curator in curators:
        logic.curator_remove(curator.user_id, course_id)
    logic.remove_course(course.course_id)
    return redirect(f'/courses/{user_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>', methods=['GET'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_editor(course_id):
    course = logic.get_course(course_id, current_user.get_id())
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.unit_type == 'test':
                test.test = logic.get_test_by_id(test.test_id)
            else:
                test.test = Test(test.test_id, course_id, TestContent(test.article_name, None))
    if course is None:
        return render_template('index.html', user=user)
    return render_template('course_editor.html', user=user, course=course)


@login_required
@courses_bp.route('/course_editor/<int:course_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_editor_save_unit(course_id):
    unit_name = request.form['newUnitName'].replace("'", '"').replace("`", '"').replace('"', '\"')
    logic.update_course_add_unit(course_id, unit_name)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/update_course/<int:course_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_update_course(course_id):
    structure = request.form.to_dict()
    course = logic.get_course(course_id, current_user.get_id())
    course.name = structure.pop('courseName')
    course.description = structure.pop('courseDesc')
    course.category = structure.pop('courseCat')
    new_units_order = []
    for unit_name, task in structure.items():
        if 'unitName' in unit_name:
            for unit in course.content['body']:
                if unit_name == 'unitName-' + str(unit['unit_id']):
                    new_units_order.append(unit)
    course.content['body'] = new_units_order
    for unit in course.content['body']:
        unit['name'] = structure.pop('unitName-' + str(unit['unit_id'])).replace("'", '"').replace("`", '"').replace('"', '\"')
        new_tests_order = []
        for unit_name, task in structure.items():
            if 'unitName' in unit_name:
                break
            task_type = task[:task.index('-')]
            task_id = task[task.index('-') + 1:]
            for test in unit['tests']:
                if test.unit_type == task_type and test.test_id == int(task_id):
                    new_tests_order.append(test)
        unit['tests'] = new_tests_order
    logic.update_course(course)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/upload_course_ava/<int:course_id>', methods=["POST", "GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_upload(course_id):
    if request.method == 'POST':
        logic.upload_course_avatar(request.files['file'], current_user, course_id)
    return redirect(f'/course_preview/{course_id}')


@login_required
@courses_bp.route('/create_course/<int:user_id>', methods=['POST'])
def handle_course_create(user_id):
    course_name = request.form['courseName']
    course_desc = request.form['description']
    course_cat = request.form['category']
    if request.files:
        course_ava = request.files['file']
    else:
        course_ava = None
    course_id = logic.add_course(course_name, course_desc, course_cat, course_ava, current_user, user_id)[2]
    logic.curator_add(user_id, course_id)
    return redirect(f'/course_preview/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_test_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        if unit_id == unit['unit_id']:
            unit_name = unit['name']
    return render_template('test_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_result_test(course_id, unit_id):
    response = logic.save_test(request.form, course_id, unit_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_editor/<int:article_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_editor(course_id, article_id):
    user = logic.get_user_by_id(current_user.get_id())
    article = logic.article_get_by_id(article_id)
    course = logic.get_course(course_id, user.user_id)
    unit_name = None
    article_name = None
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.test_id == article_id and test.unit_type == 'article':
                article_name = test.article_name.replace("'", '"').replace("`", '"').replace('"', '\"')
                unit_name = unit['name']
    return render_template('article_editor.html', user=user, course_id=course_id, course=course,
                           article=article, article_name=article_name, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_editor/<int:article_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_update(course_id, article_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    article_text = request.form['Article'].replace("'", '"').replace("`", '"').replace('"', '\"')
    article = Article(article_id=article_id, course_id=course_id, content=article_text)
    unit_id = None
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.test_id == article_id and test.unit_type == 'article':
                unit_id = unit['unit_id']
    response = logic.update_article(article, course_id, unit_id, request.form['articleName'])
    if response == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_constructor/<int:unit_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        if unit_id == unit['unit_id']:
            unit_name = unit['name']
    return render_template('article_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_save(course_id, unit_id):
    article_text = request.form['Article'].replace("'", '"').replace("`", '"').replace('"', '\"')
    article = Article(article_id=None, course_id=course_id, content=article_text)
    response = logic.article_add_article(article, course_id, unit_id, request.form['articleName'])
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/create_task/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_create_task(course_id, unit_id):
    task_type = request.form['TaskType']
    if task_type == 'test':
        return redirect(url_for('courses.handle_test_constructor', course_id=course_id, unit_id=unit_id))
    else:
        return redirect(url_for('courses.handle_article_constructor', course_id=course_id, unit_id=unit_id))


@login_required
@courses_bp.route('/course/<int:course_id>/tests/<int:test_id>', methods=["GET"])
@check_subscriber_access(current_user)
def handle_load_test(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    total_score = 0
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']
    for question in test.content.questions:
        if question.score:
            total_score += question.score
    return render_template('test.html', user=user, test=test.content, score=total_score, time=time.time(),
                           course=course, unit_name=unit_name, test_id=test_id)


@login_required
@courses_bp.route('/course/<int:course_id>/article/<int:article_id>', methods=["GET"])
@check_subscriber_access(current_user)
def handle_load_article(course_id, article_id):
    article = logic.article_get_by_id(article_id)
    article.content = markdown(article.content)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, user.user_id)
    article_name = None
    unit_name = None
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.test_id == article_id and test.unit_type == 'article':
                article_name = test.article_name.replace("'", '"').replace("`", '"').replace('"', '\"')
                unit_name = unit['name']
    return render_template('preview_article.html', user=user, course=course, article=article,
                           article_name=article_name, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_edit_test(course_id, test_id):
    test = logic.get_test_by_id(test_id=test_id)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']
    return render_template('test_editor.html', user=user, test=test.content, course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_edit_test_save(course_id, test_id):
    response = logic.edit_test(request.form, test_id, course_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/tests/<int:test_id>', methods=["POST"])
@check_subscriber_access(current_user)
def handle_check_test(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    result = logic.get_test_result(test, request.form)
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']
    completed = True
    for question in test.content.questions:
        if question.current_score is None:
            completed = False
    progress = Progress(progress_id=None, completed=completed, type='test',
                        content=test.content.toJSON(), test_id=test_id, result=result.to_json())
    logic.add_progress(course_id=course_id, user_id=user.user_id, progress=Progress.to_json(progress))

    users_progress = logic.get_progress_by_course_id_all(course_id)
    users_progress_max = {}
    for i in range(len(users_progress)):
        if int(users_progress[i].progress['test_id']) == test_id:
            users_progress[i].progress['result'] = TestResult.from_json(
                json.loads(users_progress[i].progress['result']))
            if users_progress[i].user_id not in users_progress_max.keys():
                users_progress_max[users_progress[i].user_id] = []
            users_progress_max[users_progress[i].user_id].append(
                users_progress[i].progress['result'].total_current_score)
    for key in users_progress_max.keys():
        users_progress_max[key] = max(users_progress_max[key])
    for i in range(len(users_progress)):
        if int(users_progress[i].progress['test_id']) == test_id:
            if users_progress_max[users_progress[i].user_id] == users_progress[i].progress['result'].total_current_score:
                users_progress_max[users_progress[i].user_id] = users_progress[i]
                users_progress_max[users_progress[i].user_id].progress['content'] = \
                    TestContent.from_json(users_progress_max[users_progress[i].user_id].progress['content'])

    user_progress = TestContent.from_json(progress.content)
    percents_for_tasks = {}
    for value in users_progress_max.values():
        for i in range(len(value.progress['content'].questions)):
            is_identical = True
            for j in range(len(value.progress['content'].questions[i].answers)):
                if value.progress['content'].questions[i].answers[j] != user_progress.questions[i].answers[j]:
                    is_identical = False
            if value.progress['content'].questions[i].ask not in percents_for_tasks.keys():
                percents_for_tasks[value.progress['content'].questions[i].ask] = 0
            if is_identical:
                percents_for_tasks[value.progress['content'].questions[i].ask] += 1

    for key in percents_for_tasks.keys():
        percents_for_tasks[key] -= 1
        percents_for_tasks[key] /= len(users_progress_max.keys()) - 1 if len(users_progress_max.keys()) > 1 else 1
        percents_for_tasks[key] *= 100
        percents_for_tasks[key] = round(percents_for_tasks[key], 2)
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_result.html', user=user, test=test.content, score=result.total_score, test_id=test_id,
                           total_score=result.total_current_score, result=result.result, total_time=result.total_time,
                           course=course, unit_name=unit_name, percents_for_tasks=percents_for_tasks)


@login_required
@courses_bp.route('/course/<int:course_id>/article/<int:article_id>', methods=["POST"])
@check_subscriber_access(current_user)
def handle_check_article(course_id, article_id):
    user = logic.get_user_by_id(current_user.get_id())
    progresses = logic.get_progress_by_user_course_ids_all(user.user_id, course_id)
    need_to_add = True
    for progress in progresses:
        if progress.progress['type'] == 'article' and int(progress.progress['test_id']) == article_id:
            need_to_add = False
    if need_to_add is True:
        progress = Progress(progress_id=None, completed=True, type='article',
                            content=None, test_id=article_id, result=None)
        logic.add_progress(course_id=course_id, user_id=user.user_id, progress=Progress.to_json(progress))
    return redirect(f'/course/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/test_result/<int:test_id>/<int:progress_id>', methods=["GET"])
@check_subscriber_access(current_user)
def handle_show_test_result(course_id, test_id, progress_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']
    progress = logic.get_progress_by_id(progress_id)
    progress.progress = Progress.from_json(progress.progress)
    result = TestResult.from_json(json.loads(progress.progress['result']))

    users_progress = logic.get_progress_by_course_id_all(course_id)
    users_progress_max = {}
    for i in range(len(users_progress)):
        if int(users_progress[i].progress['test_id']) == test_id:
            users_progress[i].progress['result'] = TestResult.from_json(json.loads(users_progress[i].progress['result']))
            if users_progress[i].user_id not in users_progress_max.keys():
                users_progress_max[users_progress[i].user_id] = []
            users_progress_max[users_progress[i].user_id].append(users_progress[i].progress['result'].total_current_score)
    for key in users_progress_max.keys():
        users_progress_max[key] = max(users_progress_max[key])
    for i in range(len(users_progress)):
        if int(users_progress[i].progress['test_id']) == test_id:
            if users_progress_max[users_progress[i].user_id] == users_progress[i].progress['result'].total_current_score:
                users_progress_max[users_progress[i].user_id] = users_progress[i]
                users_progress_max[users_progress[i].user_id].progress['content'] = \
                    TestContent.from_json(users_progress_max[users_progress[i].user_id].progress['content'])

    user_progress = TestContent.from_json(progress.progress['content'])
    percents_for_tasks = {}
    for value in users_progress_max.values():
        for i in range(len(value.progress['content'].questions)):
            is_identical = True
            for j in range(len(value.progress['content'].questions[i].answers)):
                if value.progress['content'].questions[i].answers[j] != user_progress.questions[i].answers[j]:
                    is_identical = False
            if value.progress['content'].questions[i].ask not in percents_for_tasks.keys():
                percents_for_tasks[value.progress['content'].questions[i].ask] = 0
            if is_identical:
                percents_for_tasks[value.progress['content'].questions[i].ask] += 1

    for key in percents_for_tasks.keys():
        percents_for_tasks[key] -= 1
        percents_for_tasks[key] /= len(users_progress_max.keys()) - 1  if len(users_progress_max.keys()) > 1 else 1
        percents_for_tasks[key] *= 100
        percents_for_tasks[key] = round(percents_for_tasks[key], 2)
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_result.html', user=user, test=user_progress, percents_for_tasks=percents_for_tasks,
                           score=result.total_score, total_score=result.total_current_score, test_id=test_id,
                           result=result.result, total_time=result.total_time, course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_check/<int:test_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_test_check_preview(course_id, test_id):
    progress = logic.get_progress_by_course_id_all(course_id)
    test = logic.get_test_by_id(test_id)
    user_id = current_user.get_id()
    course = logic.get_course(test.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    to_delete = []
    max_score = 0
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != test_id:
            to_delete.append(i)
        else:
            progress[i].progress['result'] = TestResult.from_json(json.loads(progress[i].progress['result']))
            if progress[i].progress['result'].total_current_score > max_score:
                max_score = progress[i].progress['result'].total_current_score
    for i in reversed(to_delete):
        progress.pop(i)

    users = {}
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) == test_id:
            username = logic.get_user_by_id(progress[i].user_id).username
            if username not in users.values():
                users[progress[i].user_id] = username

    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']
    return render_template('test_check_preview.html', user=user, test=test, course=course, progresses=progress,
                           users=users, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_check/<int:test_id>/<int:progress_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_test_check(course_id, test_id, progress_id):
    user = logic.get_user_by_id(current_user.get_id())
    progress = logic.get_progress_by_id(progress_id)
    username = logic.get_user_by_id(progress.user_id).username
    progress.progress = Progress.from_json(progress.progress)
    result = TestResult.from_json(json.loads(progress.progress['result']))
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = None
    for unit in course.content['body']:
        for test_ in unit['tests']:
            if test_.test_id == test_id and test_.unit_type == 'test':
                unit_name = unit['name']
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_check.html', user=user, test=TestContent.from_json(progress.progress['content']),
                           score=result.total_score, unit_name=unit_name,
                           course=course, username=username, test_id=test_id,
                           total_score=result.total_current_score, result=result.result, total_time=result.total_time)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_check/<int:test_id>/<int:progress_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_test_check_over(course_id, test_id, progress_id):
    user = logic.get_user_by_id(current_user.get_id())
    progress = logic.get_progress_by_id(progress_id)
    progress.progress = Progress.from_json(progress.progress)
    progress.progress['content'] = TestContent.from_json(progress.progress['content'])
    test = copy.deepcopy(progress.progress['content'])
    result = TestResult.from_json(json.loads(progress.progress['result']))
    comments = request.form.to_dict()
    for key, value in comments.items():
        if 'score-' not in key:
            progress.progress['content'].questions[int(key) - 1].comment = value
        else:
            if value.isdigit():
                progress.progress['content'].questions[int(key[key.index('-')+1:]) - 1].current_score = int(value)
            elif value:
                progress.progress['content'].questions[int(key[key.index('-')+1:]) - 1].current_score = float(value)
            else:
                progress.progress['content'].questions[int(key[key.index('-')+1:]) - 1].current_score = None
    new_current_score = 0
    completed = True
    for question in progress.progress['content'].questions:
        if question.current_score is not None:
            new_current_score += question.current_score
        else:
            completed = False
    progress.progress['completed'] = completed
    result.total_current_score = new_current_score
    new_result = round(new_current_score / result.total_score * 100, 2)
    result.result = new_result
    progress.progress['result'] = result.to_json()
    progress.progress['content'] = progress.progress['content'].toJSON()
    progress.progress = Progress.to_json(Progress(None, progress.progress['test_id'], progress.progress['type'],
                                                  progress.progress['completed'], progress.progress['result'],
                                                  progress.progress['content']))
    logic.update_progress(progress)
    return redirect(f'/course_editor/{course_id}/tests_check/{test_id}')
    #return render_template('test_check.html', user=user, test=test,
    #                       score=result.total_score,
    #                       total_score=result.total_current_score, result=result.result, total_time=result.total_time)


@login_required
@courses_bp.route('/course_preview/<int:course_id>')
def handle_course(course_id):
    user_id = current_user.get_id()
    course = logic.course_get_for_preview(course_id, user_id)
    reviews = logic.get_reviews_by_course_id(course_id)
    average_rate = 0
    user_review = None
    curators = logic.get_curators_by_course_id(course_id)
    if curators:
        curators = [curator.user_id for curator in curators]
        is_curator = user_id in curators
    else:
        is_curator = False
    if reviews:
        for review in reviews:
            if review.user_id == user_id:
                user_review = review
            average_rate += review.rate
        average_rate /= len(reviews)
        if len(reviews) > 5:
            reviews = random.sample(reviews, 5)
    users_for_review = {}
    if reviews:
        for review in reviews:
            users_for_review[review.user_id] = logic.get_user_by_id(review.user_id)
    return render_template('course.html', course=course, reviews=reviews, users_for_review=users_for_review,
                           user_review=user_review, average_rate=round(average_rate, 1), is_curator=is_curator)


@login_required
@courses_bp.route('/course_preview/<int:course_id>/rate_course_with_comment', methods=['POST'])
@check_subscriber_access(current_user)
def handle_rate_course(course_id):
    user_id = current_user.get_id()
    reviews = logic.get_reviews_by_course_id(course_id)
    user_rate = None
    if reviews:
        for review in reviews:
            if review.user_id == user_id:
                user_rate = review.rate
    response = logic.update_review(user_id, course_id, user_rate, request.form['rate-comment'])
    if response:
        return redirect(f'/course_preview/{course_id}')
    return flash('Ошибка при отправке отзыва', 'error')


@login_required
@courses_bp.route('/course_preview/<int:course_id>/reviews')
def handle_reviews(course_id):
    reviews = logic.get_reviews_by_course_id(course_id)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course_without_rel(course_id)
    users_for_review = {}
    if reviews:
        for review in reviews:
            users_for_review[review.user_id] = logic.get_user_by_id(review.user_id)
    return render_template('reviews.html', course=course, reviews=reviews, users_for_review=users_for_review)


@courses_bp.route('/course_participants/<int:course_id>')
@login_required
def handle_participants(course_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course_without_rel(course_id)
    participants = []
    rels = logic.get_course_rels_all(course_id)
    for rel in rels:
        participants.append(logic.get_user_by_id(rel.user_id))
    curators = logic.get_curators_by_course_id(course_id)
    if curators:
        curators = [curator.user_id for curator in curators]
        is_curator = user.user_id in curators
    else:
        is_curator = False
    for participant in participants:
        if curators and participant.user_id in curators:
            participant.is_curator = True
        else:
            participant.is_curator = False
    return render_template('participants.html', course=course, participants=participants, is_curator=is_curator)


@login_required
@courses_bp.route('/course_participants/<int:course_id>/add_curator/<int:user_id>')
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_add_curator(course_id, user_id):
    logic.curator_add(user_id, course_id)
    return redirect(f'/course_participants/{course_id}')


@login_required
@courses_bp.route('/course_participants/<int:course_id>/remove_curator/<int:user_id>')
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_remove_curator(course_id, user_id):
    logic.curator_remove(user_id, course_id)
    return redirect(f'/course_participants/{course_id}')
