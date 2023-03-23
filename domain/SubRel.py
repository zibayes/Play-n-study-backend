class SubRel:
    sub_rel_id: int = 0
    user_id: int = 0
    sub_id: int = 0

    def __init__(self, sub_rel_id, user_id, sub_id):
        self.sub_rel_id = sub_rel_id
        self.user_id = user_id
        self.sub_id = sub_id

    def json(self):
        return {
            "sub_rel_id": self.sub_rel_id,
            "user_id": self.user_id,
            "sub_id": self.sub_id
        }
