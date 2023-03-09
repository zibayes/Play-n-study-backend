class Achievement:
    ach_id: int = 0
    course_id: int = 0
    name: None
    image: None

    def __init__(self, ach_id, course_id, name, image):
        self.ach_id = ach_id
        self.course_id = course_id
        self.name = name
        self.image = image

    def json(self):
        return {
            "ach_id": self.ach_id,
            "course_id": self.course_id,
            "name": self.name,
            "image": self.image
        }