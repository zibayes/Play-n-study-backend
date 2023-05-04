from werkzeug.security import check_password_hash, generate_password_hash
from data.repositories import UserRepository
from data.types import User
from logic.auth.check import get_register_wrong_field_msg


class Auth:
    def __init__(self, session):
        self.data = UserRepository(session)

    def user_auth(self, email_or_username, password):
        user = self.data.get_user_by_email(email_or_username)
        if user is None:
            user = self.data.get_user_by_username(email_or_username)

        if user is not None and check_password_hash(user.password, password):
            return user
        return None

    def user_register(self, form):
        error = get_register_wrong_field_msg(self.data, form)
        if error is None:
            user = User(user_id=None,
                        email=form.get('email'),
                        username=form.get('username'),
                        city='',
                        avatar=None,
                        password=generate_password_hash(form.get('password')))

            if self.data.add_user(user):
                return tuple(['Вы успешно зарегистрированы', 'success'])
            return tuple(['Ошибка при add_user', 'error'])
        else:
            return tuple([error, 'error'])
