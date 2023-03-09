class Review:
    rev_id: int = 0
    user_id: int = 0
    course_id: int = 0
    rate: int = 0
    text: str = None

    def __init__(self, rev_id, user_id, course_id, rate, text):
        self.rev_id = rev_id
        self.user_id = user_id
        self.course_id = course_id
        self.rate = rate
        self.text = text

    def json(self):
        return {
            "rev_id": self.rev_id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "rate": self.rate,
            "text": self.text
        }
