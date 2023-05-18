

class UserLogin:
    def __init__(self):
        self.__user = None

    def from_db(self, logic, user_id):
        self.__user = logic.get_user_by_id(user_id)
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
        return self.__user.user_id

    def verify_ext(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False