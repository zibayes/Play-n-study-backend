import flask_login
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import redirect, render_template

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
