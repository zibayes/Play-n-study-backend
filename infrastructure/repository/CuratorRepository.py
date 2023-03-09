import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import CuratorsModel
from domain.Curator import Curator
from sqlalchemy.orm.session import Session


class CuratorRepository:
    session: Session = None

    def __init__(self, session: Session):
        self.session = session

    def add_curator(self, curator: Curator):
        try:
            new_curator = CuratorsModel(
                user_id=curator.user_id,
                course_id=curator.course_id
            )
            self.session.add(new_curator)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка при добавлении в БД " + str(e))
            return False

    def get_curators_by_course_id(self, course_id: int) -> Optional[list]:
        curators_db = self.session.query(CuratorsModel) \
            .filter_by(course_id=course_id) \
            .all()
        curators_list = []
        for curator in curators_db:
            curators_list.append(service.curator_db_to_curator(curator))
        if len(curators_list) > 0:
            return curators_list
        return None
