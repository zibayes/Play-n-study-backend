from domain.User import User
from presentation.models.models import UsersModel


def user_db_to_user(user: UsersModel) -> User:
    return User(user_id=user.user_id,
                email=user.email,
                username=user.username,
                city=user.city,
                password=user.password)
