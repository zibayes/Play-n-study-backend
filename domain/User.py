class User:
    user_id: int = 0
    email: str = None
    username: str = None
    city: str = None
    password: str = None

    # поля получаемые запросами
    achievements = None

    def __init__(self, user_id, email, username, city, password):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.city = city
        self.password = password

    def json(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "city": self.city,
            "password": self.password
        }

