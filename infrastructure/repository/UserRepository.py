import sqlalchemy.exc
import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import UsersModel
from domain.User import User
from sqlalchemy.orm.session import Session


class UserRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_user(self, user: User) -> bool:
        try:
            new_user = service.user_to_users_db(user)
            self.session.add(new_user)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

    def update_user(self, user: User) -> bool:
        try:
            self.session.query(UsersModel) \
                .filter_by(user_id=user.user_id) \
                .update({'username': user.username,
                         'email': user.email,
                         'city': user.city,
                         'password': user.password})
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления в БД " + str(e))
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

    def get_users_by_substring(self, substring: str) -> Optional[list]:
        users = []
        users_db = self.session.query(UsersModel) \
            .filter(UsersModel.username.like(substring + "%")) \
            .all()

        if users_db is not None:
            for user in users_db:
                users.append(service.user_db_to_user(user))
        if len(users) > 0:
            return users
        return None

