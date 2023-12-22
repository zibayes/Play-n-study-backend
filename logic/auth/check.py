from settings import MAX_USERNAME_LEN, MIN_PASSWORD_LEN, MIN_EMAIL_LEN, MAX_PASSWORD_LEN
from data.repositories import UserRepository
from typing import Optional
import re

def get_register_form_fields(form_fields) -> tuple:
    return form_fields['email'], form_fields['username'], \
           form_fields['password'], form_fields['password2']


def get_register_wrong_field_msg(user_repository: UserRepository, form_fields) -> Optional[str]:
    email, username,  password, password_confirm = get_register_form_fields(form_fields)
    print(username)
    if len(username) > MAX_USERNAME_LEN:
        return f'Длина ника должна быть меньше {MAX_USERNAME_LEN} символов'
    elif not re.match("^[a-zA-Z0-9_-]*$", username):
        return f'В имени пользователя не может быть специальных символов'
    elif len(password) > MAX_PASSWORD_LEN:
        return f'Длина пароля должна быть меньше {MAX_PASSWORD_LEN} символов'
    elif len(password) < MIN_PASSWORD_LEN:
        return f'Пароль должен состоять минимум из {MIN_PASSWORD_LEN} символов'
    elif len(email) < MIN_EMAIL_LEN:
        return f'Не бывает почт длинной менее {MIN_EMAIL_LEN} символов'
    elif password != password_confirm:
        return f'Пароли не совпадают'
    elif user_repository.get_user_by_username(username) is not None:
        return f'Пользователь с ником {username} уже зарегистрирован'
    elif user_repository.get_user_by_email(email) is not None:
        return f'Пользователь с почтой {email} уже зарегистрирован'
    return None


def am_i_subscriber_of(sub_to, user) -> bool:
    am_i_sub = False
    for user_in_my_list in sub_to:
        if user_in_my_list.user_id == user.user_id:
            am_i_sub = True
    return am_i_sub
