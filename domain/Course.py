class Course:
    course_id: int = 0
    name: str = None

    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name

    def json(self):
        return {
            "course_id": self.course_id,
            "name": self.name
        }
