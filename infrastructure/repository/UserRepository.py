import sqlalchemy.exc
import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import UsersModel
from domain.User import User


class UserRepository:
    session = None

    def __init__(self, session):
        self.session = session

    def add_user(self, user: User) -> bool:
        try:
            new_user = UsersModel(
                email=user.email,
                city=user.city,
                username=user.username,
                password=user.password
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

    def get_user_by_id(self, user_id) -> Optional[User]:
        user_db = self.session.query(UsersModel) \
            .filter_by(user_id=user_id) \
            .first()
        if user_db is not None:
            return service.user_db_to_user(user_db)
        return None

    def get_user_by_username(self, username) -> Optional[User]:
        user_db = self.session.query(UsersModel) \
            .filter_by(username=username) \
            .first()
        if user_db is not None:
            return service.user_db_to_user(user_db)
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_db = self.session.query(UsersModel) \
            .filter_by(email=email) \
            .first()
        if user_db is not None:
            return service.user_db_to_user(user_db)
        return None
