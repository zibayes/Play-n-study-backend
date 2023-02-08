from presentation.models.models import *
from typing import Optional


def get_user_achievements(session, user_id: int) -> Optional[list]:
    rows = session.query(UsersModel, AchievementsModel, AchieveRelModel, CoursesModel) \
        .filter(UsersModel.user_id == AchieveRelModel.user_id) \
        .filter(AchievementsModel.ach_id == AchieveRelModel.ach_id) \
        .filter(AchievementsModel.course_id == CoursesModel.course_id) \
        .filter(UsersModel.user_id == user_id).all()

    if len(rows) < 1:
        return None

    achievements = []
    i = 0
    for row in rows:
        achievements.append((row[1].name, row[3].name))

    return achievements
