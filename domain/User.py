class User:
    user_id: int = 0
    email: str = None
    username: str = None
    city: str = None
    avatar: str = None
    password: str = None

    # поля получаемые запросами
    achievements: list = None
    courses: list = None
    courses_count: int = 0
    subs: list = None
    subs_count: int = 0
    sub_to: list = None
    sub_to_count: int = 0

    def __init__(self, user_id, email, username, city, avatar, password):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.city = city
        self.avatar = avatar
        self.password = password

    def json(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "city": self.city,
            "avatar": self.avatar,
            "password": self.password
        }

