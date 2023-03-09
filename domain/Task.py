from datetime import date


class Task:
    task_id: int = 0
    user_id: int = 0
    name: str = None
    tags: list = []
    description: str = None
    date: date = None
    completed: bool = False

    def __init__(self, task_id, user_id, name, tags, description, _date, completed):
        self.task_id = task_id
        self.user_id = user_id
        self.name = name
        self.tags = tags
        self.description = description
        self.date = _date
        self.completed = completed

    def json(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "name": self.name,
            "tags": self.tags,
            "description": self.description,
            "date": self.date,
            "completed": self.completed
        }
