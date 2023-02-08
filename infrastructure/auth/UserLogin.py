from infrastructure.repository.users_repository import get_user_by_id


class UserLogin:
    def __init__(self):
        self.__user = None

    def from_db(self, session, user_id):
        self.__user = get_user_by_id(session, user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.__user['id'])
