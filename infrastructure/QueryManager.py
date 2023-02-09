from presentation.models.models import *
from typing import Optional
from infrastructure.repository.UserRepository import UserRepository


class QueryManager:
    session = None

    def __init__(self, session):
        self.session = session

    def get_user_achievements(self, user_id: int) -> Optional[list]:
        rows = self.session.query(UsersModel, AchievementsModel, AchieveRelModel, CoursesModel) \
            .filter(UsersModel.user_id == AchieveRelModel.user_id) \
            .filter(AchievementsModel.ach_id == AchieveRelModel.ach_id) \
            .filter(AchievementsModel.course_id == CoursesModel.course_id) \
            .filter(UsersModel.user_id == user_id).all()

        if len(rows) < 1:
            return None

        achievements = []
        i = 0
        # todo: append'ить ещё ссылку на изображение. Поле есть в базе просто добавьте row[i].image
        for row in rows:
            achievements.append((row[1].name, row[3].name))

        return achievements

    def get_user_courses(self, user_id: int) -> Optional[list]:
        pass
