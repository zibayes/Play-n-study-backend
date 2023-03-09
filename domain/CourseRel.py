class CourseRel:
    cour_rel_id: int = 0
    user_id: int = 0
    course_id: int = 0

    def __init__(self, cour_rel_id, user_id, course_id):
        self.cour_rel_id = cour_rel_id
        self.user_id = user_id
        self.course_id = course_id

    def json(self):
        return {
            "cour_rel_id": self.cour_rel_id,
            "user_id": self.user_id,
            "course_id": self.course_id
        }
