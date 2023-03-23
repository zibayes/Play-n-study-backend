class Course:
    course_id: int = 0
    name: str = None
    avatar: str = None

    def __init__(self, course_id, name, avatar):
        self.course_id = course_id
        self.name = name
        self.avatar = avatar

    def json(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "avatar": self.avatar
        }
