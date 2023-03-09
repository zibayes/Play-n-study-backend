import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import AchieveRelModel
from domain.AchieveRel import AchieveRel
from sqlalchemy.orm.session import Session


class AchieveRelRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_achieve_rel(self, achive_rel: AchieveRel) -> bool:
        try:
            new_ach_rel = AchieveRelModel(
                ach_id=achive_rel.ach_id,
                user_id=achive_rel.user_id
            )
            self.session.add(new_ach_rel)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления в БД " + str(e))
            return False

    def get_achive_rels_by_user_id(self, user_id) -> Optional[list]:
        new_ach_rels_db = self.session.query(AchieveRelModel) \
            .filter_by(user_id=user_id) \
            .all()
        ach_rel_list = []
        for ach_rel in new_ach_rels_db:
            ach_rel_list.append(service.ach_rel_db_to_ach_rel(ach_rel))
        if len(ach_rel_list) > 0:
            return ach_rel_list
        return None
