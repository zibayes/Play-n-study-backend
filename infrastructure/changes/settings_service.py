from settings import MAX_USERNAME_LEN, MIN_PASSWORD_LEN, MIN_EMAIL_LEN
from infrastructure.repository.UserRepository import UserRepository
from werkzeug.security import generate_password_hash
from typing import Optional



def get_wrong_field_msg(user_repository: UserRepository, user):
    if len(user.username) > MAX_USERNAME_LEN:
        return f'Длина ника должна быть меньше {MAX_USERNAME_LEN} символов'

    elif len(user.password) < MIN_PASSWORD_LEN:
        return f'Пароль должен состоять минимум из {MIN_PASSWORD_LEN} символов'

    elif len(user.email) < MIN_EMAIL_LEN:
        return f'Не бывает почт длинной менее {MIN_EMAIL_LEN} символов'

    elif user_repository.get_user_by_username(user.username) is not None:
        return f'Пользователь с ником {user.username} уже зарегистрирован'

    elif user_repository.get_user_by_email(user.email) is not None:
        return f'Пользователь с почтой {user.email} уже зарегистрирован'
    return None
