import random
import json

from flask_login import current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.types import TestContent, Test, Progress
from logic.test import TestResult
from logic.facade import LogicFacade
from markdown import markdown

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)


def specify_tests_for_view(course, course_id, progresses=None):
    results = {}
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.unit_type == 'test':
                test.test = logic.get_test_by_id(test.test_id)
            elif test.unit_type in ('article', 'file_attach'):
                article = logic.article_get_by_id(test.test_id)
                test.test = Test(test.test_id, course_id, test.unit_id, TestContent(article.name, None),
                                 description=article.description, avatar=article.avatar)
            elif test.unit_type == 'link':
                link = logic.link_get_by_id(test.test_id)
                test.test = Test(test.test_id, course_id, test.unit_id, TestContent(link.name, None),
                                 avatar=link.avatar, description=link.link)
            elif test.unit_type == 'forum':
                forum = logic.forum_get_by_id(test.test_id)
                test.test = Test(test.test_id, course_id, test.unit_id, TestContent(forum.name, None),
                                 avatar=forum.avatar, description=forum.description)
            if progresses:
                for progress in progresses:
                    if progress.progress['test_id'] == test.test_id and progress.progress['type'] == test.unit_type:
                        results[str(test.test_id) + test.unit_type] = progress.progress['completed']
    if progresses:
        return results


def get_tests_data(course_id):
    course = logic.get_course(course_id, current_user.get_id())
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    if course is None:
        return user
    progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
    results = specify_tests_for_view(course, course_id, progresses)
    return user, course, results, progresses


def get_unit_name(course, task_id, task_type):
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.test_id == task_id and test.unit_type == task_type:
                return unit['name']


def get_unit_name_by_id(course, unit_id):
    for unit in course.content['body']:
        if unit_id == unit['unit_id']:
            return unit['name']


def get_unit_id(course, task_id, task_type):
    for unit in course.content['body']:
        for test in unit['tests']:
            if test.test_id == task_id and test.unit_type == task_type:
                return unit['unit_id']


def delete_unit_task(course_id, task_id):
    user_id = current_user.get_id()
    course = logic.get_course(course_id, user_id)
    index_to_delete = 0
    inner_index_to_delete = 0
    is_break = False
    for unit in course.content['body']:
        for test in unit['tests']:
            if int(test.test_id) == task_id:
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
        if int(progress.progress['test_id']) == task_id:
            logic.remove_progress(progress.up_id)


def get_test(test, shuffle):
    total_score = 0
    completed = True
    for question in test.content.questions:
        if question.score:
            total_score += question.score
        if question.shuffle == 'on' and shuffle:
            if question.type == 'compliance':
                answers = {}
                for item in question.answers:
                    answers = dict(list(answers.items()) + list(item.items()))
                question.answers = answers
                # question.answers = dict(list(question.answers.items()) + list(question.answers.items()))
                question.answers = dict(zip(question.answers, random.sample(list(question.answers.values()),
                                                                            len(question.answers))))
                answers = []
                for item in question.answers.items():
                    answers.append({item[0]: item[1]})
                question.answers = answers
            else:
                random.shuffle(question.answers)
        question.ask = markdown(question.ask)
        if question.answers:
            for i in range(len(question.answers)):
                if question.type not in ('filling_gaps', 'drag_to_text', 'markers_drag', 'free'):
                    print(question.answers[i])
                    key = list(question.answers[i].keys())[0]
                    tmp = question.answers[i][list(question.answers[i].keys())[0]]
                    del question.answers[i][list(question.answers[i].keys())[0]]
                    question.answers[i][markdown(key)] = tmp

        if question.current_score is None:
            completed = False
    return total_score, completed


def get_test_result(course_id, test_id, progress):
    users_progress = logic.get_progress_by_course_id_all(course_id)
    users_progress_max = {}
    for i in range(len(users_progress)):
        if int(users_progress[i].progress['test_id']) == test_id and users_progress[i].progress['result']:
            users_progress[i].progress['result'] = TestResult.from_json(
                json.loads(users_progress[i].progress['result']))
            if users_progress[i].user_id not in users_progress_max.keys():
                users_progress_max[users_progress[i].user_id] = []
            users_progress_max[users_progress[i].user_id].append(
                users_progress[i].progress['result'].total_current_score)
    for key in users_progress_max.keys():
        users_progress_max[key] = max(users_progress_max[key])
    for i in range(len(users_progress)):
        if int(users_progress[i].progress['test_id']) == test_id and users_progress[i].progress['result']:
            if users_progress_max[users_progress[i].user_id] == users_progress[i].progress[
                'result'].total_current_score:
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
        percents_for_tasks[key] -= 1 if percents_for_tasks[key] > 0 else 0
        percents_for_tasks[key] /= len(users_progress_max.keys()) - 1 if len(users_progress_max.keys()) > 1 else 1
        percents_for_tasks[key] *= 100
        percents_for_tasks[key] = round(percents_for_tasks[key], 2)
    return percents_for_tasks, user_progress


def course_update(course, request):
    structure = request.form.to_dict()
    course.name = structure.pop('courseName')
    course.description = structure.pop('courseDesc')
    course.category = structure.pop('courseCat')
    if request.files['file']:
        course.avatar = logic.upload_course_avatar(request.files['file'], current_user)
    new_units_order = []
    for unit_name, task in structure.items():
        if 'unitName' in unit_name:
            for unit in course.content['body']:
                if unit_name == 'unitName-' + str(unit['unit_id']):
                    new_units_order.append(unit)
    course.content['body'] = new_units_order
    for unit in course.content['body']:
        unit['name'] = structure.pop('unitName-' + str(unit['unit_id'])).replace("'", '"').replace("`", '"').replace(
            '"', '\"')
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


def get_course_summary(course, progresses, user):
    marks = {}
    max_marks = {}
    units_max = {}
    units_cur = {}
    for progress in progresses:
        if progress.progress['result']:
            progress.progress['result'] = TestResult.from_json(json.loads(progress.progress['result']))
            if (str(progress.progress['test_id']) + progress.progress['type']) not in marks.keys():
                marks[str(progress.progress['test_id']) + progress.progress['type']] = []
                max_marks[str(progress.progress['test_id']) + progress.progress['type']] = progress.progress[
                    'result'].total_score
            marks[str(progress.progress['test_id']) + progress.progress['type']].append(
                progress.progress['result'].total_current_score)
    for key in marks.keys():
        marks[key] = max(marks[key])
    total = sum(marks.values())
    total_max = sum(max_marks.values())

    for unit in course.content['body']:
        first_time = True
        for test in unit['tests']:
            units_cur_score = 0
            units_max_score = 0
            for progress in progresses:
                if progress.progress['result']:
                    if (str(test.test_id) + test.unit_type) == (
                            str(progress.progress['test_id']) + progress.progress['type']):
                        if first_time:
                            units_max[unit['unit_id']] = 0
                            first_time = False
                        if unit['unit_id'] not in units_cur.keys():
                            units_cur[unit['unit_id']] = 0
                            units_cur_score = progress.progress['result'].total_current_score
                        else:
                            if units_cur_score < progress.progress[
                                'result'].total_current_score:  # TODO: Проверить корректность данного алгоритма (один раз уже проверено и исправлено)
                                units_cur_score = progress.progress['result'].total_current_score
                        units_max_score = progress.progress['result'].total_score
            if unit['unit_id'] in units_cur.keys():
                units_cur[unit['unit_id']] += units_cur_score
                units_max[unit['unit_id']] += units_max_score

    leaders = logic.get_progress_by_course_id_all(course.course_id)
    # leaders = progresses
    leaders_to_show = {}
    leaders_total_score = {}
    leaders_hrefs = {}
    graphic_data = {}
    friends = {}
    subs = logic.get_user_for_subscriptions(user.user_id).sub_to
    if subs:
        subs = [user.username for user in subs]
    for unit in course.content['body']:
        for test in unit['tests']:
            for i in range(len(leaders)):
                if (str(test.test_id) + test.unit_type) == (str(leaders[i].progress['test_id']) + leaders[i].progress['type']) \
                        and leaders[i].progress['result']:
                    leaders[i].progress['result'] = TestResult.from_json(json.loads(leaders[i].progress['result']))
                    user_for_table = logic.get_user_by_id(leaders[i].user_id).username
                    if user_for_table not in leaders_to_show.keys():
                        leaders_to_show[user_for_table] = {}
                        leaders_hrefs[user_for_table] = leaders[i].user_id
                        leaders_total_score[user_for_table] = {}
                        if subs and user_for_table in subs or user_for_table == user.username:
                            friends[user_for_table] = []
                    if (str(test.test_id) + test.unit_type) not in leaders_to_show[user_for_table].keys():
                        leaders_to_show[user_for_table][str(test.test_id) + test.unit_type] = []
                    leaders_to_show[user_for_table][str(test.test_id) + test.unit_type].append(leaders[i].progress['result'].total_current_score)
                    leaders_total_score[user_for_table][str(test.test_id) + test.unit_type] = float(leaders[i].progress['result'].total_score)

    for key in leaders_to_show.keys():
        sum_all = 0
        leaders_total_score[key] = sum(leaders_total_score[key].values())
        for task in leaders_to_show[key].keys():
            sum_all += max(leaders_to_show[key][task])
        leaders_to_show[key] = sum_all
        for friend in friends.keys():
            friends[friend] = leaders_to_show[friend]
        if leaders_to_show[key] not in graphic_data.keys():
            graphic_data[leaders_to_show[key]] = 0
        graphic_data[leaders_to_show[key]] += 1

    return units_cur, units_max, marks, max_marks, total, total_max, \
        leaders_total_score, graphic_data, leaders_to_show, leaders_hrefs, friends


def get_test_preview(progress, course_id, test_id, user):
    to_delete = []
    max_score = 0
    max_score_total = 0
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != test_id or progress[i].task_type != 'test' or not progress[i].progress['result']:
            to_delete.append(i)
        else:
            progress[i].progress['result'] = TestResult.from_json(json.loads(progress[i].progress['result']))
            if progress[i].progress['result'].total_current_score > max_score:
                max_score = progress[i].progress['result'].total_current_score
                max_score_total = progress[i].progress['result'].total_score
    for i in reversed(to_delete):
        progress.pop(i)

    leaders = logic.get_progress_by_course_id_all(course_id)
    leaders_to_show = {}
    leaders_total_score = {}
    leaders_hrefs = {}
    graphic_data = {}
    friends = {}
    subs = logic.get_user_for_subscriptions(user.user_id).sub_to
    if subs:
        subs = [user.username for user in subs]
    for i in range(len(leaders)):
        if int(leaders[i].progress['test_id']) == test_id and leaders[i].progress['result']:
            leaders[i].progress['result'] = TestResult.from_json(json.loads(leaders[i].progress['result']))
            user_for_table = logic.get_user_by_id(leaders[i].user_id).username
            if user_for_table not in leaders_to_show.keys():
                leaders_to_show[user_for_table] = []
                leaders_hrefs[user_for_table] = leaders[i].user_id
                leaders_total_score[user_for_table] = leaders[i].progress['result'].total_score
                if subs and user_for_table in subs or user_for_table == user.username:
                    friends[user_for_table] = []
            leaders_to_show[user_for_table].append(leaders[i].progress['result'].total_current_score)
            if leaders_to_show[user_for_table][-1] == max(leaders_to_show[user_for_table]):
                leaders_total_score[user_for_table] = leaders[i].progress['result'].total_score

            if subs and user_for_table in subs or user_for_table == user.username:
                friends[user_for_table].append(leaders[i].progress['result'].total_current_score)
    for key in leaders_to_show.keys():
        leaders_to_show[key] = max(leaders_to_show[key])
        if key in friends.keys():
            friends[key] = max(friends[key])
        if leaders_to_show[key] not in graphic_data.keys():
            graphic_data[leaders_to_show[key]] = 0
        graphic_data[leaders_to_show[key]] += 1
    print(leaders_to_show)
    return max_score_total, leaders_total_score, max_score, graphic_data, leaders_to_show, leaders_hrefs, friends


def check_test_over(progress, request):
    progress.progress = Progress.from_json(progress.progress)
    progress.progress['content'] = TestContent.from_json(progress.progress['content'])
    result = TestResult.from_json(json.loads(progress.progress['result']))
    comments = request.form.to_dict()
    for key, value in comments.items():
        if 'score-' not in key:
            progress.progress['content'].questions[int(key) - 1].comment = value
        else:
            if value.isdigit():
                progress.progress['content'].questions[int(key[key.index('-') + 1:]) - 1].current_score = int(value)
            elif value:
                progress.progress['content'].questions[int(key[key.index('-') + 1:]) - 1].current_score = float(value)
            else:
                progress.progress['content'].questions[int(key[key.index('-') + 1:]) - 1].current_score = None
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


def get_file_attach_preview(progress, course_id, article_id, user):
    to_delete = []
    max_score = 0
    max_score_total = 0
    for i in range(len(progress)):
        if int(progress[i].progress['test_id']) != article_id or progress[i].task_type != 'file_attach':
            to_delete.append(i)
        else:
            progress[i].progress['result'] = TestResult.from_json(json.loads(progress[i].progress['result']))
            if progress[i].progress['result'].total_current_score > max_score:
                max_score = progress[i].progress['result'].total_current_score
                max_score_total = progress[i].progress['result'].total_score
    for i in reversed(to_delete):
        progress.pop(i)

    leaders = logic.get_progress_by_course_id_all(course_id)
    leaders_to_show = {}
    leaders_total_score = {}
    leaders_hrefs = {}
    graphic_data = {}
    friends = {}
    subs = logic.get_user_for_subscriptions(user.user_id).sub_to
    if subs:
        subs = [user.username for user in subs]
    for i in range(len(leaders)):
        if int(leaders[i].progress['test_id']) == article_id and leaders[i].progress['result']:
            leaders[i].progress['result'] = TestResult.from_json(json.loads(leaders[i].progress['result']))
            user_for_table = logic.get_user_by_id(leaders[i].user_id).username
            if user_for_table not in leaders_to_show.keys():
                leaders_to_show[user_for_table] = []
                leaders_hrefs[user_for_table] = leaders[i].user_id
                leaders_total_score[user_for_table] = leaders[i].progress['result'].total_score
                if subs and user_for_table in subs or user_for_table == user.username:
                    friends[user_for_table] = []
            leaders_to_show[user_for_table].append(leaders[i].progress['result'].total_current_score)
            if leaders_to_show[user_for_table][-1] == max(leaders_to_show[user_for_table]):
                leaders_total_score[user_for_table] = leaders[i].progress['result'].total_score

            if subs and user_for_table in subs or user_for_table == user.username:
                friends[user_for_table].append(leaders[i].progress['result'].total_current_score)
    for key in leaders_to_show.keys():
        leaders_to_show[key] = max(leaders_to_show[key])
        if key in friends.keys():
            friends[key] = max(friends[key])
        if leaders_to_show[key] not in graphic_data.keys():
            graphic_data[leaders_to_show[key]] = 0
        graphic_data[leaders_to_show[key]] += 1
    return max_score_total, leaders_total_score, max_score, graphic_data, leaders_to_show, leaders_hrefs, friends


def get_forum_structure(ft_id, forum_id, course_id):
    messages = logic.messages_get_all_by_topic_id(ft_id)
    messages_ordered = []
    nesting_level = {None: 0}
    users = {}
    for message in messages:
        if message.user_id not in users.keys():
            users[message.user_id] = logic.get_user_by_id(message.user_id)
        if message.parent_tm_id in nesting_level.keys():
            nesting_level[message.tm_id] = nesting_level[message.parent_tm_id] + 1
    msgs = {}
    for message in messages:
        if message.parent_tm_id not in msgs.keys():
            msgs[message.parent_tm_id] = [message.tm_id]
        elif message.tm_id not in msgs[message.parent_tm_id]:
            msgs[message.parent_tm_id].append(message.tm_id)
    ordered_msgs = []
    if msgs:
        ordered_msgs = msgs.pop(None)
    while msgs:
        new_list = ordered_msgs
        to_del = None
        for i in range(len(ordered_msgs)):
            if ordered_msgs[i] in msgs.keys():
                j = new_list.index(ordered_msgs[i])+1
                new_list = ordered_msgs[:j] + msgs[ordered_msgs[i]] + ordered_msgs[j:]
                to_del = ordered_msgs[i]
                break
        ordered_msgs = new_list
        msgs.pop(to_del)
    for msg in ordered_msgs:
        for message in messages:
            if msg == message.tm_id:
                messages_ordered.append(message)

    users_score = {}
    for user_id in users.keys():
        all_progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
        for progress in all_progresses:
            if progress.task_type == 'forum' and progress.task_id == forum_id:
                if progress.progress['result']:
                    users_score[user_id] = json.loads(progress.progress['result'])
                else:
                    users_score[user_id] = {'total_current_score': 0}
    return users, users_score, nesting_level, messages_ordered