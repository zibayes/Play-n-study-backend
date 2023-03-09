class AchieveRel:
    ach_rel_id: int = 0
    ach_id: int = 0
    user_id: int = 0

    def __init__(self, ach_rel_id, ach_id, user_id):
        self.ach_rel_id = ach_rel_id
        self.ach_id = ach_id
        self.user_id = user_id

    def json(self):
        return {
            "ach_rel_id": self.ach_rel_id,
            "ach_id": self.ach_id,
            "user_id": self.user_id
        }
