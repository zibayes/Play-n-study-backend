import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import SubRelModel
from domain.SubRel import SubRel
from sqlalchemy.orm.session import Session


class SubRelRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_sub_rel(self, sub_rel: SubRel) -> bool:
        try:
            new_sub_rel = SubRelModel(
                user_id=sub_rel.user_id,
                sub_id=sub_rel.sub_id
            )
            self.session.add(new_sub_rel)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления в БД + " + str(e))

    def get_all_by_user_id(self, user_id: int) -> Optional[list]:
        sub_rel_db = self.session.query(SubRelModel) \
            .filter_by(user_id=user_id) \
            .all()
        subs_list = []
        for sub in sub_rel_db:
            subs_list.append(service.sub_db_to_sub(sub))
        if len(subs_list) > 0:
            return subs_list
        return None

    def get_all_by_sub_id(self, sub_id) -> Optional[list]:
        sub_rel_db = self.session.query(SubRelModel) \
            .filter_by(sub_id=sub_id) \
            .all()
        sub_to_list = []
        for sub in sub_rel_db:
            sub_to_list.append(service.sub_db_to_sub(sub))
        if len(sub_to_list) > 0:
            return sub_to_list
        return None

    def get_one_by_user_and_sub_ids(self, user_id, sub_id):
        sub_rel_db = self.session.query(SubRelModel) \
            .filter_by(user_id=user_id) \
            .filter_by(sub_id=sub_id) \
            .first()
        return service.sub_db_to_sub(sub_rel_db)

    def remove_sub_rel_by_id(self, sub_rel_id) -> bool:
        try:
            self.session.query(SubRelModel) \
                .filter_by(sub_rel_id=sub_rel_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления отношения sub_rel :" + str(e))
            return False
