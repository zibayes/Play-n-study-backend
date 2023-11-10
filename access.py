import flask_login
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import redirect, render_template
from data.types import TestContent, Test

from data.repositories import RoleRepository, CuratorRepository, CourseRepository
from logic.facade import LogicFacade

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)
role_repository = RoleRepository(session)
curator_repository = CuratorRepository(session)
course_repository = CourseRepository(session)

admin_permissions = [
    'admin.handle_admin_add_curator',
    'admin.handle_admin_remove_curator',
    '',
]
another_role_permissions = [

]

permissions = {
    "admin": admin_permissions,
    "another_role": another_role_permissions,
}


def check_access(current_user, request):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_id = current_user.get_id()
            command = request.url_rule.endpoint

            roles = role_repository.get_user_roles_by_id(user_id)

            # admin has all permissions
            if "admin" in roles:
                return func(*args, **kwargs)

            allowed = []
            for role in roles:
                allowed += permissions[role]

            if command in allowed:
                return func(*args, **kwargs)

            return seal()

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def seal():
    return "Не разрешено"


def check_curator_access(current_user):
    def decorator(func):
        def wrapper(course_id, *args, **kwargs):
            user_id = current_user.get_id()

            is_curator = curator_repository.is_user_curator_of_course(user_id, course_id)

            if is_curator:
                return func(course_id, *args, **kwargs)

            course = logic.get_course_without_rel(course_id)
            access_denied = "Вы не являетесь куратором " \
                            "курса «" + course.name + "», поэтому у вас нет доступа к данной странице"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=False)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def check_subscriber_access(current_user):
    def decorator(func):
        def wrapper(course_id, *args, **kwargs):
            user_id = current_user.get_id()

            course = logic.course_get_for_preview(course_id, user_id)
            is_subscriber = not course.can_subscribe

            if is_subscriber:
                return func(course_id, *args, **kwargs)

            course = logic.get_course_without_rel(course_id)
            access_denied = "Вы не являетесь участником " \
                            "курса «" + course.name + "», поэтому у вас нет доступа к данной странице"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=True)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def check_test_access(current_user):
    def decorator(func):
        def wrapper(course_id, test_id, *args, **kwargs):
            user_id = current_user.get_id()
            course = logic.get_course_without_rel(course_id)
            progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
            access= get_progress(course, progresses, test_id, 'test')
            if access:
                return func(course_id, test_id, *args, **kwargs)
            task_name = logic.get_test_by_id(test_id).content.name
            access_denied = "Ваш прогресс на " \
                            "курсе «" + course.name + "» ещё не достаточен для получения доступа к тесту «" + task_name + "»"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=False, not_enough=True)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def check_article_access(current_user):
    def decorator(func):
        def wrapper(course_id, article_id, *args, **kwargs):
            user_id = current_user.get_id()
            course = logic.get_course_without_rel(course_id)
            progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
            access = get_progress(course, progresses, article_id, 'article')
            if access:
                return func(course_id, article_id, *args, **kwargs)
            task_name = logic.article_get_by_id(article_id).name
            access_denied = "Ваш прогресс на " \
                            "курсе «" + course.name + "» ещё не достаточен для получения доступа к статье «" + task_name + "»"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=False, not_enough=True)
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def check_link_access(current_user):
    def decorator(func):
        def wrapper(course_id, link_id, *args, **kwargs):
            user_id = current_user.get_id()
            course = logic.get_course_without_rel(course_id)
            progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
            access = get_progress(course, progresses, link_id, 'link')
            if access:
                return func(course_id, link_id, *args, **kwargs)
            task_name = logic.link_get_by_id(link_id).name
            access_denied = "Ваш прогресс на " \
                            "курсе «" + course.name + "» ещё не достаточен для получения доступа к ссылке «" + task_name + "»"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=False, not_enough=True)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator

def check_file_attach_access(current_user):
    def decorator(func):
        def wrapper(course_id, article_id, *args, **kwargs):
            user_id = current_user.get_id()
            progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
            course = logic.get_course_without_rel(course_id)
            access = get_progress(course, progresses, article_id, 'file_attach')
            if access:
                return func(course_id, article_id, *args, **kwargs)
            task_name = logic.article_get_by_id(article_id).name
            access_denied = "Ваш прогресс на " \
                            "курсе «" + course.name + "» ещё не достаточен для получения доступа к заданию «" + task_name + "»"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=False, not_enough=True)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator

def check_forum_access(current_user):
    def decorator(func):
        def wrapper(course_id, forum_id, *args, **kwargs):
            user_id = current_user.get_id()
            progresses = logic.get_progress_by_user_course_ids_all(user_id, course_id)
            course = logic.get_course_without_rel(course_id)
            access = get_progress(course, progresses, forum_id, 'forum')
            if access:
                return func(course_id, forum_id, *args, **kwargs)
            task_name = logic.forum_get_by_id(forum_id).name
            access_denied = "Ваш прогресс на " \
                            "курсе «" + course.name + "» ещё не достаточен для получения доступа к форуму «" + task_name + "»"
            return render_template('access_denied.html', course=course, access_denied=access_denied,
                                   need_subscription=False, not_enough=True)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator

def get_progress(course, progresses, task_id, task_type):
    results = {}
    first_task = None
    for unit in course.content['body']:
        for test in unit['tests']:
            if first_task is None:
                first_task = str(test.test_id) + test.unit_type
            for progress in progresses:
                if progress.progress['test_id'] == test.test_id and progress.progress['type'] == test.unit_type:
                    results[str(test.test_id) + test.unit_type] = progress.progress['completed']
                elif str(test.test_id) + test.unit_type not in results.keys():
                    results[str(test.test_id) + test.unit_type] = False
    if str(task_id) + task_type in results.keys() and results[str(task_id) + task_type]:
        return True
    if not results and not (first_task[-len(task_type):] == task_type and int(first_task[:-len(task_type)]) == task_id):
        return False
    not_allowed = False
    for key, value in results.items():
        if key[-len(task_type):] == task_type and int(key[:-len(task_type)]) == task_id and not_allowed:
            return False
        if not value:
            not_allowed = True
    return True