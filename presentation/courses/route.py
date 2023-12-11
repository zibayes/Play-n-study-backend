import copy
import os
import random
import shutil
import time
import json
from pathlib import Path

from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.types import User, Progress, TestContent, Test, Article, Link, FileAttach, Forum, ForumTopic, TopicMessage, \
    Achievement
from logic.test import TestResult
from logic.facade import LogicFacade
from logic.course_route_functions import get_tests_data, get_unit_name, get_unit_name_by_id, get_unit_id, \
    delete_unit_task, get_test, get_test_result, course_update, get_course_summary, get_test_preview, \
    check_test_over, get_file_attach_preview, get_forum_structure
from markdown import markdown
from access import check_curator_access, check_subscriber_access, check_test_access, \
    check_article_access, check_link_access, check_file_attach_access, check_forum_access, \
    check_achievements_conditions

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
@check_achievements_conditions(current_user)
def handle_tests(course_id):
    data = get_tests_data(course_id)
    if not isinstance(data, tuple):
        render_template('index.html', user=data)
    user, course, results, _ = data
    return render_template('tests.html', user=user, course=course, results=results)


@login_required
@courses_bp.route('/course/<int:course_id>/summary')
@check_subscriber_access(current_user)
def handle_course_summary(course_id):
    data = get_tests_data(course_id)
    if not isinstance(data, tuple):
        render_template('index.html', user=data)
    user, course, results, progresses = data
    progress = logic.get_progress_by_user_course_ids_all(user.user_id, course_id)
    units_cur, units_max, marks, max_marks, total, total_max = get_course_summary(course, progresses)
    max_score_total, leaders_total_score, max_score, graphic_data, leaders_to_show, leaders_hrefs, friends = get_test_preview(progress, course_id, 3, user)
    return render_template('course_summary.html', user=user, course=course, results=results, units_cur=units_cur,
                           units_max=units_max, marks=marks, max_marks=max_marks, total=total, total_max=total_max,
                           max_score_total=max_score_total, leaders_total_score=leaders_total_score, max_score=max_score,
                           graphic_data=graphic_data, leaders=dict(sorted(leaders_to_show.items(), key=lambda item: item[1], reverse=True)), leaders_hrefs=leaders_hrefs, friends=friends)


@login_required
@courses_bp.route('/course_achievements/<int:course_id>', methods=['GET'])
@check_subscriber_access(current_user)
def handle_course_achievements(course_id):
    achivements = logic.get_achievements_by_course_id(course_id)
    achs = []
    data = get_tests_data(course_id)
    if not isinstance(data, tuple):
        render_template('index.html', user=data)
    user, course, _, _ = data
    curators = logic.get_curators_by_course_id(course_id)
    if curators:
        curators = [curator.user_id for curator in curators]
        is_curator = user.user_id in curators
    else:
        is_curator = False
    units = course.content['body']
    tests = []
    for unit in units:
        for test in unit['tests']:
            tests.append(test.test.content.name)
    for ach in achivements:
        conditions = ach.condition.split(']][[')
        reached = logic.achive_rel_exist(ach.ach_id, user.user_id)
        ach_to_add = {'ach_id': ach.ach_id, 'name': ach.name, 'description': ach.description, 'conditions': [], 'reached': reached}
        for cond in conditions:
            condition = {}
            cond = cond.replace('[[', '').replace(']]', '')
            if 'score' in cond:
                condition['condition'] = 'score'
                cond = cond.replace('score', '')
                if ' > ' in cond:
                    condition['val_amount'] = '>'
                    cond = cond.replace(' > ', '')
                elif ' = ' in cond:
                    condition['val_amount'] = '='
                    cond = cond.replace(' = ', '')
                elif ' < ' in cond:
                    condition['val_amount'] = '<'
                    cond = cond.replace(' < ', '')
                condition['value'] = cond[:cond.find(' for ')]
                cond = cond[cond.find(' for '):]
            elif 'completion fact' in cond:
                condition['condition'] = 'completion fact'
            elif 'time spent' in cond:
                condition['condition'] = 'time spent'
                cond = cond.replace('time spent', '')
                condition['time'] = cond[:cond.find(' for ')]
                cond = cond[cond.find(' for '):]
            cond = cond.replace(condition['condition'], '')
            if 'tasks' in cond:
                condition['task_category'] = 'tasks'
                cond = cond.replace(' for tasks:', '')
            elif 'units' in cond:
                condition['task_category'] = 'units'
                cond = cond.replace(' for units:', '')
            condition['tasks'] = []
            for task in cond.split(';'):
                if task != ' ':
                    condition['tasks'].append(task)
            ach_to_add['conditions'].append(condition)
        achs.append(ach_to_add)
    return render_template('course_achievements.html', user=user, course=course, units=units,
                           tests=tests, achievements=achs, is_curator=is_curator)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/edit_achievements', methods=['GET'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_edit_achievements(course_id):
    data = get_tests_data(course_id)
    if not isinstance(data, tuple):
        render_template('index.html', user=data)
    user, course, _, _ = data
    units = course.content['body']
    tests = []
    for unit in units:
        for test in unit['tests']:
            tests.append(test.test.content.name)
    return render_template('achievement_constructor.html', user=user, course=course, units=units, tests=tests)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/edit_achievements', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_save_achievements(course_id):
    avatar = None
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    conditions = request.form.getlist('condition')
    task_categories = request.form.getlist('task_category')
    value_amounts = request.form.getlist('value_amount')
    values = request.form.getlist('value')
    times = request.form.getlist('time')
    tasks = copy.deepcopy(request.form.to_dict())
    str_condition = ''
    for condition in conditions:
        if condition == 'Количество баллов':
            str_condition += '[[score'
            val_amount = value_amounts.pop(0)
            if val_amount == 'Больше':
                str_condition += ' > '
            elif val_amount == 'Равно':
                str_condition += ' = '
            elif val_amount == 'Меньше':
                str_condition += ' < '
            str_condition += values.pop(0)
        elif condition == 'Факт прохождения':
            str_condition += '[[completion fact'
        elif condition == 'Затраченное время на прохождение':
            str_condition += '[[time spent '
            str_condition += times.pop(0)
        task_category = task_categories.pop(0)
        if task_category == 'Задание':
            str_condition += ' for tasks:'
        elif task_category == 'Раздел':
            str_condition += ' for units:'
        current_part = True
        tasks_tmp = copy.deepcopy(tasks)
        for name, value in tasks.items():
            if value != 'on' and current_part:
                continue
            elif value == 'on':
                str_condition += name + '; '
                tasks_tmp.pop(name)
                current_part = False
            else:
                break
        tasks = copy.deepcopy(tasks_tmp)
        str_condition += ']]'
    achievement = Achievement(course_id=course_id, name=request.form['achievementName'],
                              description=request.form['achievementDesc'], condition=str_condition, image=avatar)
    logic.add_achievement(achievement)
    return redirect(f'/course_editor/{course_id}/edit_achievements')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/achievements/<int:ach_id>', methods=['GET'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_edit_achievement(course_id, ach_id):
    data = get_tests_data(course_id)
    if not isinstance(data, tuple):
        render_template('index.html', user=data)
    user, course, _, _ = data
    ach = logic.get_achievement_by_id(ach_id)
    ach_to_add = {'ach_id': ach.ach_id, 'name': ach.name, 'description': ach.description, 'conditions': []}
    conditions = ach.condition.split(']][[')
    for cond in conditions:
        condition = {}
        cond = cond.replace('[[', '').replace(']]', '')
        if 'score' in cond:
            condition['condition'] = 'score'
            cond = cond.replace('score', '')
            if ' > ' in cond:
                condition['val_amount'] = '>'
                cond = cond.replace(' > ', '')
            elif ' = ' in cond:
                condition['val_amount'] = '='
                cond = cond.replace(' = ', '')
            elif ' < ' in cond:
                condition['val_amount'] = '<'
                cond = cond.replace(' < ', '')
            condition['value'] = cond[:cond.find(' for ')]
            cond = cond[cond.find(' for '):]
        elif 'completion fact' in cond:
            condition['condition'] = 'completion fact'
        elif 'time spent' in cond:
            condition['condition'] = 'time spent'
            cond = cond.replace('time spent', '')
            condition['time'] = cond[:cond.find(' for ')]
            cond = cond[cond.find(' for '):]
        cond = cond.replace(condition['condition'], '')
        if 'tasks' in cond:
            condition['task_category'] = 'tasks'
            cond = cond.replace(' for tasks:', '')
        elif 'units' in cond:
            condition['task_category'] = 'units'
            cond = cond.replace(' for units:', '')
        condition['tasks'] = []
        for task in cond.split(';'):
            if task != ' ':
                condition['tasks'].append(task)
        ach_to_add['conditions'].append(condition)
    units = course.content['body']
    tests = []
    for unit in units:
        for test in unit['tests']:
            tests.append(test.test.content.name)
    return render_template('achievement_editor.html', user=user, course=course, units=units,
                           tests=tests, achievement=ach_to_add)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/achievements/<int:ach_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_save_achievement(course_id, ach_id):
    avatar = None
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    else:
        avatar =logic.get_achievement_by_id(ach_id).image
    conditions = request.form.getlist('condition')
    task_categories = request.form.getlist('task_category')
    value_amounts = request.form.getlist('value_amount')
    values = request.form.getlist('value')
    times = request.form.getlist('time')
    tasks = copy.deepcopy(request.form.to_dict())
    str_condition = ''
    for condition in conditions:
        if condition == 'Количество баллов':
            str_condition += '[[score'
            val_amount = value_amounts.pop(0)
            if val_amount == 'Больше':
                str_condition += ' > '
            elif val_amount == 'Равно':
                str_condition += ' = '
            elif val_amount == 'Меньше':
                str_condition += ' < '
            str_condition += values.pop(0)
        elif condition == 'Факт прохождения':
            str_condition += '[[completion fact'
        elif condition == 'Затраченное время на прохождение':
            str_condition += '[[time spent '
            str_condition += times.pop(0)
        task_category = task_categories.pop(0)
        if task_category == 'Задание':
            str_condition += ' for tasks:'
        elif task_category == 'Раздел':
            str_condition += ' for units:'
        current_part = True
        tasks_tmp = copy.deepcopy(tasks)
        for name, value in tasks.items():
            if value != 'on' and current_part:
                continue
            elif value == 'on':
                str_condition += name + '; '
                tasks_tmp.pop(name)
                current_part = False
            else:
                break
        tasks = copy.deepcopy(tasks_tmp)
        str_condition += ']]'
    achievement = Achievement(ach_id=ach_id, course_id=course_id, name=request.form['achievementName'],
                              description=request.form['achievementDesc'], condition=str_condition, image=avatar)
    logic.update_achievement(achievement)
    return redirect(f'/course_achievements/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/achievements_delete/<int:ach_id>', methods=['GET'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_course_delete_achievement(course_id, ach_id):
    ach_rels = logic.get_achive_rels_by_achievement_id(ach_id)
    if ach_rels:
        for ach_rel in ach_rels:
            logic.remove_achive_rel(ach_rel.ach_rel_id)
    logic.remove_achievement(ach_id)
    return redirect(f'/course_achievements/{course_id}')


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
@check_test_access(current_user)
def handle_test_preview(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user_id = current_user.get_id()
    course = logic.get_course(test.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    unit_name = get_unit_name(course, test_id, 'test')
    progress = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    max_score_total, leaders_total_score, max_score, graphic_data, leaders_to_show, leaders_hrefs, friends = get_test_preview(progress, course_id, test_id, user)
    return render_template("test_preview.html", user=user, test=test, course=course, unit_name=unit_name, max_score_total=max_score_total, leaders_total_score=leaders_total_score,
                           progresses=progress, max_score=max_score, graphic_data=dict(sorted(graphic_data.items(), key=lambda item: item[0], reverse=False)),
                           leaders=dict(sorted(leaders_to_show.items(), key=lambda item: item[1], reverse=True)), leaders_hrefs=leaders_hrefs, friends=friends)


@login_required
@courses_bp.route('/delete_test/<int:course_id>/<int:test_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_test(course_id, test_id):
    delete_unit_task(course_id, test_id)
    logic.remove_test(test_id)
    abs_path = str(Path(__file__).absolute())
    abs_path = abs_path[:abs_path.find('\\presentation\\') + len('/presentation/')]
    path = abs_path + 'static/users_files/' + str(test_id) + 'test/'
    shutil.rmtree(path)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/delete_article/<int:course_id>/<int:article_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_article(course_id, article_id):
    delete_unit_task(course_id, article_id)
    logic.remove_article(article_id)
    abs_path = str(Path(__file__).absolute())
    abs_path = abs_path[:abs_path.find('\\presentation\\') + len('/presentation/')]
    path = abs_path + 'static/users_files/' + str(article_id) + 'file_attach/'
    shutil.rmtree(path)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/delete_link/<int:course_id>/<int:link_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_link(course_id, link_id):
    delete_unit_task(course_id, link_id)
    logic.remove_link(link_id)
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/delete_forum/<int:course_id>/<int:forum_id>', methods=['POST'])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_delete_forum(course_id, forum_id):
    delete_unit_task(course_id, forum_id)
    logic.remove_forum(forum_id)
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
        elif test.unit_type in ('article', 'file_attach'):
            logic.remove_article(test.test_id)
        elif test.unit_type == 'link':
            logic.remove_link(test.test_id)
        elif test.unit_type == 'forum':
            topics = logic.topic_get_all_by_forum_id(test.test_id)
            for topic in topics:
                messages = logic.messages_get_all_by_topic_id(topic.ft_id)
                for msg in messages:
                    logic.remove_topic_message(msg.tm_id)
                logic.remove_forum_topic(topic.ft_id)
            logic.remove_forum(test.test_id)
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
            elif test.unit_type in ('article', 'file_attach'):
                logic.remove_article(test.test_id)
            elif test.unit_type == 'link':
                logic.remove_link(test.test_id)
            elif test.unit_type == 'forum':
                topics = logic.topic_get_all_by_forum_id(test.test_id)
                for topic in topics:
                    messages = logic.messages_get_all_by_topic_id(topic.ft_id)
                    for msg in messages:
                        logic.remove_topic_message(msg.tm_id)
                    logic.remove_forum_topic(topic.ft_id)
                logic.remove_forum(test.test_id)
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
    data = get_tests_data(course_id)
    if not isinstance(data, tuple):
        render_template('index.html', user=data)
    user, course, _, _ = data
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
    course = logic.get_course(course_id, current_user.get_id())
    course_update(course, request)
    logic.update_course(course)
    return redirect(f'/course_editor/{course_id}')


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
    unit_name = get_unit_name_by_id(course, unit_id)
    return render_template('test_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/test_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_result_test(course_id, unit_id):
    response = logic.save_test(request.form, request.files, course_id, unit_id)
    test_id = logic.data.get_last_test_by_course(course_id).test_id
    for filename, file in request.files.to_dict().items():
        if 'File-' in filename:
            abs_path = str(Path(__file__).absolute())
            abs_path = abs_path[:abs_path.find('\\presentation\\') + len('/presentation/')]
            path = abs_path + 'static/users_files/' + str(test_id) + 'test/'
            Path(path).mkdir(parents=True, exist_ok=True)
            file.save(os.path.join(path, filename + file.filename[file.filename.rfind('.'):]))
    if request.files['file']:
        logic.upload_test_avatar(request.files['file'], current_user, test_id)
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
    unit_name= get_unit_name(course, article_id, 'article')
    return render_template('article_editor.html', user=user, course_id=course_id, course=course,
                           article=article, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_editor/<int:article_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_update(course_id, article_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    article_text = request.form['Article'].replace("'", '"').replace("`", '"').replace('"', '\"')
    unit_id = get_unit_id(course, article_id, 'article')
    avatar = logic.article_get_by_id(article_id).avatar
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    article = Article(article_id=article_id, course_id=course_id, content=article_text, unit_id=unit_id, name=request.form['articleName'],
                      description=request.form['articleDesc'], avatar=avatar, score=None)
    response = logic.update_article(article, course_id, unit_id, 'article')
    if response == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении статьи', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_constructor/<int:unit_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name_by_id(course, unit_id)
    return render_template('article_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/article_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_article_save(course_id, unit_id):
    article_text = request.form['Article'].replace("'", '"').replace("`", '"').replace('"', '\"')
    avatar = None
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    article = Article(article_id=None, course_id=course_id, unit_id=unit_id, content=article_text, name=request.form['articleName'],
                      description=request.form['articleDesc'], avatar=avatar, score=None)
    response = logic.article_add_article(article, course_id, unit_id, 'article')
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении статьи', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/create_task/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_create_task(course_id, unit_id):
    if 'TaskType' not in request.form.keys():
        return redirect(f'/course_editor/{course_id}')
    task_type = request.form['TaskType']
    if task_type == 'test':
        return redirect(url_for('courses.handle_test_constructor', course_id=course_id, unit_id=unit_id))
    elif task_type == 'article':
        return redirect(url_for('courses.handle_article_constructor', course_id=course_id, unit_id=unit_id))
    elif task_type == 'link':
        return redirect(url_for('courses.handle_link_constructor', course_id=course_id, unit_id=unit_id))
    elif task_type == 'file_attach':
        return redirect(url_for('courses.handle_file_attach_constructor', course_id=course_id, unit_id=unit_id))
    elif task_type == 'forum':
        return redirect(url_for('courses.handle_forum_constructor', course_id=course_id, unit_id=unit_id))


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_constructor/<int:unit_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_forum_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name_by_id(course, unit_id)
    return render_template('forum_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_forum_save(course_id, unit_id):
    avatar = None
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    forum = Forum(forum_id=None, course_id=course_id, unit_id=unit_id, name=request.form['forumName'],
                  description=request.form['forumDesc'], avatar=avatar, score=request.form['score'])
    response = logic.forum_add_forum(forum)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении форума', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_editor/<int:forum_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_forum_editor(course_id, forum_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_id = get_unit_id(course, forum_id, 'forum')
    unit_name = get_unit_name_by_id(course, unit_id)
    forum = logic.forum_get_by_id(forum_id)
    return render_template('forum_editor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name, forum=forum)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_editor/<int:forum_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_forum_update(course_id, forum_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    unit_id = get_unit_id(course, forum_id, 'forum')
    avatar = logic.forum_get_by_id(forum_id).avatar
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    forum = Forum(forum_id=forum_id, course_id=course_id, unit_id=unit_id, name=request.form['forumName'],
                  description=request.form['forumDesc'], avatar=avatar, score=request.form['score'])
    response = logic.update_forum(forum)
    if response == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении форума', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/forum_list/<int:forum_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_load_forum_topics(course_id, forum_id):
    forum = logic.forum_get_by_id(forum_id)
    topics = logic.topic_get_all_by_forum_id(forum_id)
    last_messages = {}
    for topic in topics:
        message = logic.get_last_message_by_topic(topic.ft_id)
        if message:
            user = logic.get_user_by_id(message.user_id)
            last_messages[topic.ft_id] = {'message': message, 'user': user}
        else:
            last_messages[topic.ft_id] = None
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, user.user_id)
    unit_name = get_unit_name(course, forum_id, 'forum')
    all_progresses = logic.get_progress_by_user_course_ids_all(user.user_id, course_id)
    user_score = None
    for progress in all_progresses:
        if progress.task_type == 'forum' and progress.task_id == forum_id and progress.progress['result']:
            user_score = json.loads(progress.progress['result'])['total_current_score']
    return render_template('forum_list.html', user=user, course=course, forum=forum, user_score=user_score,
                           topics=topics, unit_name=unit_name, last_messages=last_messages)


@login_required
@courses_bp.route('/course/<int:course_id>/forum_list/<int:forum_id>', methods=["POST"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_add_forum_topic(course_id, forum_id):
    topic = ForumTopic(ft_id=None, forum_id=forum_id, name=request.form['newTopicName'], is_active=True)
    logic.forum_topic_add_forum_topic(topic)
    return redirect(f'/course/{course_id}/forum_list/{forum_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/forum_list/<int:forum_id>/search', methods=["POST"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_find_forum_topic(course_id, forum_id):
    query = request.form['query']
    if len(query) > 0:
        forum = logic.forum_get_by_id(forum_id)
        topics = logic.get_topics_by_query(query, forum_id)
        last_messages = {}
        if not topics:
            topics = []
        for topic in topics:
            message = logic.get_last_message_by_topic(topic.ft_id)
            if message:
                user = logic.get_user_by_id(message.user_id)
                last_messages[topic.ft_id] = {'message': message, 'user': user}
            else:
                last_messages[topic.ft_id] = None

        user = logic.get_user_by_id(current_user.get_id())
        course = logic.get_course(course_id, user.user_id)
        unit_name = get_unit_name(course, forum_id, 'forum')
        return render_template('forum_list.html', user=user, course=course, forum=forum,
                               topics=topics, unit_name=unit_name, last_messages=last_messages)
    return redirect(f'/course/{course_id}/forum_list/{forum_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/forum_list/<int:forum_id>/forum/<int:ft_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_load_forum_topic(course_id, forum_id, ft_id):
    forum = logic.forum_get_by_id(forum_id)
    topic = logic.forum_topic_get_by_id(ft_id)
    users, users_score, nesting_level, messages_ordered = get_forum_structure(ft_id, forum_id, course_id)
    user = logic.get_user_by_id(current_user.get_id())
    users_score = None
    if users_score and user.user_id in users_score.keys():
        users_score = users_score[user.user_id]['total_current_score']
    course = logic.get_course(course_id, user.user_id)
    unit_name = get_unit_name(course, forum_id, 'forum')
    return render_template('forum.html', user=user, course=course, forum=forum, nesting_level=nesting_level,
                           topic=topic, unit_name=unit_name, messages=messages_ordered,
                           users=users, user_score=users_score)


@login_required
@courses_bp.route('/course/<int:course_id>/forum_list/<int:forum_id>/forum/<int:ft_id>', methods=["POST"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_topic_send_message(course_id, forum_id, ft_id):
    msg = request.form.to_dict()
    message = None
    for key, value in msg.items():
        if key[8:] == 'None':
            key = None
        else:
            key = key[8:]
        message = TopicMessage(tm_id=None, ft_id=ft_id, parent_tm_id=key, user_id=current_user.get_id(), tm_date=None, content=value)
    logic.add_topic_message(message)

    task_type = 'forum'
    user_id = current_user.get_id()
    all_progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    is_done = False
    for progress in all_progresses:
        if progress.task_type == task_type and progress.task_id == forum_id:
            is_done = True
    if not is_done:
        progress = Progress(progress_id=None, completed=True, type=task_type,
                            content=None, test_id=forum_id, result=None)
        logic.add_progress(course_id=course_id, user_id=user_id, task_type=task_type, task_id=forum_id,
                           progress=Progress.to_json(progress))
    return redirect(f'/course/{course_id}/forum_list/{forum_id}/forum/{ft_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_check/<int:forum_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_load_forum_topics_editor(course_id, forum_id):
    forum = logic.forum_get_by_id(forum_id)
    topics = logic.topic_get_all_by_forum_id(forum_id)
    last_messages = {}
    if not topics:
        topics = []
    for topic in topics:
        message = logic.get_last_message_by_topic(topic.ft_id)
        if message:
            user = logic.get_user_by_id(message.user_id)
            last_messages[topic.ft_id] = {'message': message, 'user': user}
        else:
            last_messages[topic.ft_id] = None
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, user.user_id)
    unit_name = get_unit_name(course, forum_id, 'forum')
    return render_template('forum_list_check.html', user=user, course=course, forum=forum,
                           topics=topics, unit_name=unit_name, last_messages=last_messages)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_list_check/<int:forum_id>/search', methods=["POST"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_find_forum_topic_check(course_id, forum_id):
    query = request.form['query']
    if len(query) > 0:
        forum = logic.forum_get_by_id(forum_id)
        topics = logic.get_topics_by_query(query, forum_id)
        last_messages = {}
        for topic in topics:
            message = logic.get_last_message_by_topic(topic.ft_id)
            if message:
                user = logic.get_user_by_id(message.user_id)
                last_messages[topic.ft_id] = {'message': message, 'user': user}
            else:
                last_messages[topic.ft_id] = None
        user = logic.get_user_by_id(current_user.get_id())
        course = logic.get_course(course_id, user.user_id)
        unit_name = get_unit_name(course, forum_id, 'forum')
        return render_template('forum_list_check.html', user=user, course=course, forum=forum,
                               topics=topics, unit_name=unit_name, last_messages=last_messages)
    return redirect(f'/course_editor/{course_id}/forum_check/{forum_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_check/<int:forum_id>/forum/<int:ft_id>', methods=["POST"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_send_forum_topic_check(course_id, forum_id, ft_id):
    marks = request.form.to_dict()
    users_score = {}
    for id, mark in marks.items():
        if 'score-' in id:
            users_score[id[6:]] = mark
    for user_id, mark in users_score.items():
        all_progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
        for progress in all_progresses:
            if progress.task_type == 'forum' and progress.task_id == forum_id:
                progress.progress['result'] = TestResult(logic.forum_get_by_id(forum_id).score,
                                                         float(mark), None, None).to_json()
                progress.progress = Progress.to_json(
                    Progress(None, progress.progress['test_id'], progress.progress['type'], #progress.progress['progress_id']
                             progress.progress['completed'], progress.progress['result'],
                             progress.progress['content']))
                logic.update_progress(progress)
    return redirect(f'/course_editor/{course_id}/forum_check/{forum_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_check/<int:forum_id>/forum/<int:ft_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_load_forum_topic_check(course_id, forum_id, ft_id):
    forum = logic.forum_get_by_id(forum_id)
    topic = logic.forum_topic_get_by_id(ft_id)
    users, users_score, nesting_level, messages_ordered = get_forum_structure(ft_id, forum_id, course_id)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, user.user_id)
    unit_name = get_unit_name(course, forum_id, 'forum')
    return render_template('forum_check.html', user=user, course=course, forum=forum, nesting_level=nesting_level,
                           topic=topic, unit_name=unit_name, messages=messages_ordered, users=users, users_score=users_score)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_check/<int:forum_id>/forum/<int:ft_id>/open', methods=["GET"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_open_forum_topic(course_id, forum_id, ft_id):
    topic = logic.forum_topic_get_by_id(ft_id)
    topic.is_active = True
    logic.update_forum_topic(topic)
    return redirect(f'/course_editor/{course_id}/forum_check/{forum_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/forum_check/<int:forum_id>/forum/<int:ft_id>/close', methods=["GET"])
@check_subscriber_access(current_user)
@check_forum_access(current_user)
def handle_close_forum_topic(course_id, forum_id, ft_id):
    topic = logic.forum_topic_get_by_id(ft_id)
    topic.is_active = False
    logic.update_forum_topic(topic)
    return redirect(f'/course_editor/{course_id}/forum_check/{forum_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/link_constructor/<int:unit_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_link_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name_by_id(course, unit_id)
    return render_template('link_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/link_editor/<int:link_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_link_editor(course_id, link_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_id = get_unit_id(course, link_id, 'link')
    unit_name = get_unit_name_by_id(course, unit_id)
    link = logic.link_get_by_id(link_id)
    return render_template('link_editor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name, link=link)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/link_editor/<int:link_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_link_update(course_id, link_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    unit_id = get_unit_id(course, link_id, 'link')
    avatar = logic.link_get_by_id(link_id).avatar
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    link = Link(link_id=link_id, course_id=course_id, unit_id=unit_id, name=request.form['linkName'], link=request.form['link'], avatar=avatar)
    response = logic.update_link(link)
    if response == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении ссылки', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/link_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_link_save(course_id, unit_id):
    avatar = None
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    link = Link(link_id=None, course_id=course_id, unit_id=unit_id, name=request.form['linkName'], link=request.form['link'], avatar=avatar)
    response = logic.link_add_link(link, course_id, unit_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении ссылки', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_constructor/<int:unit_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_constructor(course_id, unit_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name_by_id(course, unit_id)
    return render_template('file_attach_constructor.html', user=user, course_id=course_id, unit_id=unit_id,
                           course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_constructor/<int:unit_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_save(course_id, unit_id):
    article_text = request.form['Article'].replace("'", '"').replace("`", '"').replace('"', '\"')
    avatar = None
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    article = Article(article_id=None, course_id=course_id, unit_id=unit_id, content=article_text, name=request.form['articleName'],
                      description=request.form['articleDesc'], avatar=avatar, score=request.form['score'])
    response = logic.article_add_article(article, course_id, unit_id, 'file_attach')
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении задания с прикреплением файла', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_editor/<int:article_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_editor(course_id, article_id):
    user = logic.get_user_by_id(current_user.get_id())
    article = logic.article_get_by_id(article_id)
    course = logic.get_course(course_id, user.user_id)
    score = 0
    unit_name = get_unit_name(course, article_id, 'file_attach')
    return render_template('file_attach_editor.html', user=user, course_id=course_id, course=course,
                           article=article, unit_name=unit_name, score=score)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_editor/<int:article_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_update(course_id, article_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    article_text = request.form['Article'].replace("'", '"').replace("`", '"').replace('"', '\"')
    unit_id = get_unit_id(course, article_id, 'file_attach')
    avatar = logic.article_get_by_id(article_id).avatar
    if request.files['file']:
        avatar = logic.upload_course_avatar(request.files['file'], current_user)
    article = Article(article_id=article_id, course_id=course_id, content=article_text, unit_id=unit_id, name=request.form['articleName'],
                      description=request.form['articleDesc'], avatar=avatar, score=request.form['score'])
    response = logic.update_article(article=article, course_id=course_id, unit_id=unit_id, task_type='file_attach')
    if response == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении задания', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/file_attach_preview/<int:article_id>')
@check_subscriber_access(current_user)
@check_file_attach_access(current_user)
def handle_file_attach_preview(course_id, article_id):
    article = logic.article_get_by_id(article_id)
    user_id = current_user.get_id()
    course = logic.get_course(article.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    unit_name = get_unit_name(course, article_id, 'file_attach')
    progress = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    max_score_total, leaders_total_score, max_score, graphic_data, leaders_to_show, leaders_hrefs, friends = get_file_attach_preview(progress, course_id, article_id, user)
    return render_template("file_attach_preview.html", user=user, article=article, course=course, unit_name=unit_name, max_score_total=max_score_total, leaders_total_score=leaders_total_score,
                           progresses=progress, max_score=max_score, graphic_data=dict(sorted(graphic_data.items(), key=lambda item: item[0], reverse=False)),
                           leaders=dict(sorted(leaders_to_show.items(), key=lambda item: item[1], reverse=True)), leaders_hrefs=leaders_hrefs, friends=friends)


@login_required
@courses_bp.route('/course/<int:course_id>/file_attach_result/<int:article_id>/<int:progress_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_file_attach_access(current_user)
def handle_show_file_attach_result(course_id, article_id, progress_id):
    user = logic.get_user_by_id(current_user.get_id())
    article = logic.article_get_by_id(article_id)
    article.content = markdown(article.content)
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name(course, article_id, 'file_attach')
    progress = logic.get_progress_by_id(progress_id)
    progress.progress = Progress.from_json(progress.progress)
    result = json.loads(progress.progress['content'])
    for file in result:
        file['name'] = file['file_path'][file['file_path'].rfind('/')+1:]
        file[0] = file['file_path'][file['file_path'].rfind('static'):]
    # result = TestResult.from_json(json.loads(progress.progress['result']))
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('file_attach_result.html', user=user, article=article,
                           course=course, unit_name=unit_name, result=result)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_check/<int:article_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_check_preview(course_id, article_id):
    progress = logic.get_progress_by_course_id_all(course_id)
    article = logic.article_get_by_id(article_id)
    user_id = current_user.get_id()
    course = logic.get_course(article.course_id, user_id)
    user = logic.get_user_by_id(user_id)
    to_delete = []
    max_score = 0
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != article_id or progress[i].task_type != 'file_attach':
            to_delete.append(i)
        else:
            pass
            '''progress[i].progress['result'] = TestResult.from_json(json.loads(progress[i].progress['result']))
            if progress[i].progress['result'].total_current_score > max_score:
                max_score = progress[i].progress['result'].total_current_score'''
    for i in reversed(to_delete):
        progress.pop(i)

    users = {}
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) == article_id:
            username = logic.get_user_by_id(progress[i].user_id).username
            if username not in users.values():
                users[progress[i].user_id] = username

    unit_name = get_unit_name(course, article_id, 'file_attach')
    return render_template('file_attach_check_preview.html', user=user, article=article, course=course, progresses=progress,
                           users=users, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_check/<int:article_id>/<int:progress_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_check(course_id, article_id, progress_id):
    user = logic.get_user_by_id(current_user.get_id())
    progress = logic.get_progress_by_id(progress_id)
    username = logic.get_user_by_id(progress.user_id).username
    progress.progress = Progress.from_json(progress.progress)
    # result = TestResult.from_json(json.loads(progress.progress['result']))
    result = json.loads(progress.progress['content'])
    for file in result:
        file['name'] = file['file_path'][file['file_path'].rfind('/') + 1:]
        file[0] = file['file_path'][file['file_path'].rfind('static'):]
    res = json.loads(progress.progress['result'])
    current_score = res['total_current_score']
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name(course, article_id, 'file_attach')
    article = logic.article_get_by_id(article_id)
    article.content = markdown(article.content)
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('file_attach_check.html', user=user, article=article,
                           unit_name=unit_name, current_score=current_score,
                           course=course, username=username, article_id=article_id, result=result)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/file_attach_check/<int:article_id>/<int:progress_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_file_attach_check_over(course_id, article_id, progress_id):
    progress = logic.get_progress_by_id(progress_id)
    progress.progress['result'] = TestResult(logic.article_get_by_id(article_id).score,
                                             float(request.form['current_score']), None, None).to_json()
    progress.progress = Progress.to_json(Progress(None, progress.progress['test_id'], progress.progress['type'],
                                                  progress.progress['completed'], progress.progress['result'],
                                                  progress.progress['content']))
    logic.update_progress(progress)
    return redirect(f'/course_editor/{course_id}/file_attach_check/{article_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/file_attach/<int:article_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_file_attach_access(current_user)
def handle_load_file_attach(course_id, article_id):
    article = logic.article_get_by_id(article_id)
    article.content = markdown(article.content)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, user.user_id)
    unit_name = get_unit_name(course, article_id, 'file_attach')
    return render_template('file_attach.html', user=user, course=course, article=article, unit_name=unit_name)


@login_required
@courses_bp.route('/course/<int:course_id>/file_attach/<int:article_id>', methods=["POST"])
@check_subscriber_access(current_user)
@check_file_attach_access(current_user)
def handle_upload_file_attach(course_id, article_id):
    user = logic.get_user_by_id(current_user.get_id())
    files = []
    # result = TestResult(total_score=None, total_current_score=None, total_time=None, result=None)
    progress = Progress(progress_id=None, completed=True, type='file_attach',
                        content=json.dumps(files), test_id=article_id, result=None)
    logic.add_progress(course_id=course_id, user_id=user.user_id, task_type='file_attach', task_id=article_id,
                       progress=Progress.to_json(progress))
    if request.files['file']:
        progress = logic.get_last_progress_by_task(user.user_id, course_id, article_id, 'file_attach')
        for file in request.files.getlist('file'):
            abs_path = str(Path(__file__).absolute())
            abs_path = abs_path[:abs_path.find('\\presentation\\') + len('/presentation/')]
            path = abs_path + 'static/users_files/' + str(article_id) + 'file_attach/' + str(progress.up_id) + '/'
            Path(path).mkdir(parents=True, exist_ok=True)
            file.save(os.path.join(path, file.filename))
            files.append({'file_path': path + '/' + file.filename, 'type': 'file'})
        progress.progress['content'] = json.dumps(files)
        progress.progress = Progress.to_json(Progress(None, progress.progress['test_id'], progress.progress['type'],
                                                      progress.progress['completed'], progress.progress['result'],
                                                      progress.progress['content']))
        logic.update_progress(progress)
    return redirect(f'/course/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/tests/<int:test_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_test_access(current_user)
def handle_load_test(course_id, test_id):
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name(course, test_id, 'test')
    total_score, _ = get_test(test, shuffle=True)
    return render_template('test.html', user=user, test=test.content, score=total_score, time=time.time(),
                           course=course, unit_name=unit_name, test_id=test_id)


@login_required
@courses_bp.route('/course/<int:course_id>/article/<int:article_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_article_access(current_user)
def handle_load_article(course_id, article_id):
    article = logic.article_get_by_id(article_id)
    article.content = markdown(article.content)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, user.user_id)
    unit_name = get_unit_name(course, article_id, 'article')
    return render_template('preview_article.html', user=user, course=course, article=article, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["GET"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_edit_test(course_id, test_id):
    test = logic.get_test_by_id(test_id=test_id)
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name(course, test_id, 'test')
    return render_template('test_editor.html', user=user, test_id=test_id, test_tmp=test, test=test.content, course=course, unit_name=unit_name)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_edit/<int:test_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_edit_test_save(course_id, test_id):
    course = logic.get_course(course_id, current_user.get_id())
    unit_id = get_unit_id(course, test_id, 'test')
    response = logic.edit_test(request.form, request.files, test_id, course_id, unit_id)
    for filename, file in request.files.to_dict().items():
        if 'File-' in filename:
            abs_path = str(Path(__file__).absolute())
            abs_path = abs_path[:abs_path.find('\\presentation\\') + len('/presentation/')]
            path = abs_path + 'static/users_files/' + str(test_id) + 'test/'
            Path(path).mkdir(parents=True, exist_ok=True)
            file.save(os.path.join(path, filename + file.filename[file.filename.rfind('.'):]))
    if request.files['file']:
        logic.upload_test_avatar(request.files['file'], current_user, test_id)
    if response[1] == 'success':
        return redirect(f'/course_editor/{course_id}')
    flash('Ошибка при сохранении теста', 'error')
    return redirect(f'/course_editor/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/tests/<int:test_id>', methods=["POST"])
@check_subscriber_access(current_user)
@check_test_access(current_user)
def handle_check_test(course_id, test_id):
    task_type = 'test'
    test = logic.get_test_by_id(test_id)
    user = logic.get_user_by_id(current_user.get_id())
    result = logic.get_test_result(test, request.form)
    _, completed = get_test(test, shuffle=False)
    progress = Progress(progress_id=None, completed=completed, type=task_type,
                        content=test.content.toJSON(), test_id=test_id, result=result.to_json())
    logic.add_progress(course_id=course_id, user_id=user.user_id, task_type=task_type, task_id=test_id, progress=Progress.to_json(progress))
    progress = logic.get_last_progress_by_task(user.user_id, course_id, test_id, task_type)
    return redirect(f'/course/{course_id}/test_result/{test_id}/{progress.up_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/article/<int:article_id>', methods=["POST"])
@check_subscriber_access(current_user)
@check_article_access(current_user)
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
        logic.add_progress(course_id=course_id, user_id=user.user_id, task_type='article', task_id=article_id, progress=Progress.to_json(progress))
    return redirect(f'/course/{course_id}')


@login_required
@courses_bp.route('/course/<int:course_id>/link/<int:link_id>', methods=["GET"])
@check_subscriber_access(current_user)
@check_link_access(current_user)
def handle_use_link(course_id, link_id):
    user = logic.get_user_by_id(current_user.get_id())
    progresses = logic.get_progress_by_user_course_ids_all(user.user_id, course_id)
    need_to_add = True
    for progress in progresses:
        if progress.progress['type'] == 'link' and int(progress.progress['test_id']) == link_id:
            need_to_add = False
    if need_to_add is True:
        progress = Progress(progress_id=None, completed=True, type='link',
                            content=None, test_id=link_id, result=None)
        logic.add_progress(course_id=course_id, user_id=user.user_id, task_type='link', task_id=link_id, progress=Progress.to_json(progress))
    link = logic.link_get_by_id(link_id)
    return redirect(link.link)


@login_required
@courses_bp.route('/course/<int:course_id>/test_result/<int:test_id>/<int:progress_id>', methods=["GET"])
@check_achievements_conditions(current_user)
@check_subscriber_access(current_user)
@check_test_access(current_user)
def handle_show_test_result(course_id, test_id, progress_id):
    user = logic.get_user_by_id(current_user.get_id())
    course = logic.get_course(course_id, current_user.get_id())
    unit_name = get_unit_name(course, test_id, 'test')
    progress = logic.get_progress_by_id(progress_id)
    progress.progress = Progress.from_json(progress.progress)
    result = TestResult.from_json(json.loads(progress.progress['result']))
    percents_for_tasks, user_progress = get_test_result(course_id, test_id, progress)
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
        if int(progress[i].progress['test_id']) != test_id or not progress[i].progress['result']:
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

    unit_name = get_unit_name(course, test_id, 'test')
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
    unit_name = get_unit_name(course, test_id, 'test')
    test = TestContent.from_json(progress.progress['content'])
    # todo: передавать score, result, total_score, total_time - объект result и парсить его шаблонизатором
    return render_template('test_check.html', user=user, test=test,
                           score=result.total_score, unit_name=unit_name,
                           course=course, username=username, test_id=test_id,
                           total_score=result.total_current_score, result=result.result, total_time=result.total_time)


@login_required
@courses_bp.route('/course_editor/<int:course_id>/tests_check/<int:test_id>/<int:progress_id>', methods=["POST"])
@check_curator_access(current_user)
@check_subscriber_access(current_user)
def handle_test_check_over(course_id, test_id, progress_id):
    progress = logic.get_progress_by_id(progress_id)
    check_test_over(progress, request)
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
