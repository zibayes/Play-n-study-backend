from settings import MAX_USERNAME_LEN, MIN_PASSWORD_LEN, MIN_EMAIL_LEN
from infrastructure.repository.users_repository import get_user_by_email, get_user_by_username
from typing import Optional
from werkzeug.datastructures import MultiDict
from werkzeug.security import generate_password_hash


def get_register_form_fields(form_fields: MultiDict[str, str]) -> tuple:
    return form_fields['email'], form_fields['username'], \
           form_fields['password'], form_fields['password2']


def get_fields_for_register(form_fields: MultiDict[str, str]) -> tuple:
    fields_arr = list(get_register_form_fields(form_fields))[:3]
    fields_arr[-1] = generate_password_hash(fields_arr[-1])
    return tuple(fields_arr)


def get_register_wrong_field_msg(session, form_fields: MultiDict[str, str]) -> Optional[str]:
    email, username,  password, password_confirm = get_register_form_fields(form_fields)

    if len(username) > MAX_USERNAME_LEN:
        return f'Длина ника должна быть меньше {MAX_USERNAME_LEN} символов'

    elif len(password) < MIN_PASSWORD_LEN:
        return f'Пароль должен состоять минимум из {MIN_PASSWORD_LEN} символов'

    elif len(email) < MIN_EMAIL_LEN:
        return f'Не бывает почт длинной менее {MIN_EMAIL_LEN} символов'

    elif password != password_confirm:
        return f'Пароли не совпадают'

    elif get_user_by_username(session, username) is not None:
        return f'Пользователь с ником {username} уже зарегистрирован'

    elif get_user_by_email(session, email) is not None:
        return f'Пользователь с почтой {email} уже зарегистрирован'

    return None
