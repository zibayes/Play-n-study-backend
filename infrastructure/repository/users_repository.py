import sqlalchemy.exc
import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import UsersModel


def add_user(session, email, username, password, city="") -> bool:
    try:
        new_user = UsersModel(
            email=email,
            city=city,
            username=username,
            password=password
        )
        session.add(new_user)
        session.commit()
        return True
    except sqlalchemy.exc.DatabaseError as e:
        print("Ошибка добавления пользователя в БД " + str(e))
        return False


def get_user_by_id(session, user_id) -> Optional[dict]:
    user = session.query(UsersModel) \
        .filter_by(user_id=user_id) \
        .first()
    if user is not None:
        return service.user_to_json(user)
    return None


def get_user_by_username(session, username) -> Optional[dict]:
    user = session.query(UsersModel) \
        .filter_by(username=username) \
        .first()
    if user is not None:
        return service.user_to_json(user)
    return None


def get_user_by_email(session, email: str) -> Optional[dict]:
    user = session.query(UsersModel) \
        .filter_by(email=email) \
        .first()
    if user is not None:
        return service.user_to_json(user)
    return None
