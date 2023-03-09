import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import TasksModel
from domain.Task import Task
from sqlalchemy.orm.session import Session


class TaskRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_task(self, task: Task) -> bool:
        try:
            new_task = TasksModel(
                user_id=task.user_id,
                name=task.name,
                tags=task.tags,
                description=task.description,
                date=task.date,
                completed=False
            )
            self.session.add(task)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления в БД " + str(e))
            return False

    def get_tasks_by_user_id(self, user_id: int) -> Optional[list]:
        tasks_db = self.session.query(TasksModel) \
            .filter_by(user_id=user_id) \
            .all()
        tasks_list = []
        for task in tasks_db:
            tasks_list.append(service.task_db_to_task(task))
        if len(tasks_list) > 0:
            return tasks_list
        return None
