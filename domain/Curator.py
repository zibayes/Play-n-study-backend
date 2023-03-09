class Curator:
    cur_id: int = 0
    user_id: int = 0
    course_id: int = 0

    def __init__(self, cur_id, user_id, course_id):
        self.cur_id = cur_id
        self.user_id = user_id
        self.course_id = course_id

    def json(self):
        return {
            "cur_id": self.cur_id,
            "user_id": self.user_id,
            "course_id": self.course_id
        }
