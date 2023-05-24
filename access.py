import flask_login
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.repositories import RoleRepository

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

role_repository = RoleRepository(session)


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
