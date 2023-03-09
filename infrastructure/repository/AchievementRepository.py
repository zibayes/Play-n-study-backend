import sqlalchemy.exc
import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import AchievementsModel
from domain.Achievement import Achievement
from sqlalchemy.orm.session import Session


class AchievementRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_achievement(self, achievement: Achievement) -> bool:
        try:
            new_achievement = AchievementsModel(
                course_id=achievement.course_id,
                name=achievement.name,
                image=achievement.image
            )
            self.session.add(new_achievement)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавление пользователя в БД " + str(e))
            return False

    def get_achievement_by_id(self, ach_id) -> Optional[Achievement]:
        ach_db = self.session.query(AchievementsModel) \
            .filter_by(ach_id=ach_id) \
            .first()
        if ach_db is not None:
            return service.achievement_db_to_achievemnt(ach_db)
        return None
