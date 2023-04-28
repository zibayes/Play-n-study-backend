import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import TestsModel
from domain.Test import Test, TestContent
from sqlalchemy.orm.session import Session


class TestRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def get_test_by_id(self, test_id):
        test_db = self.session.query(TestsModel) \
            .filter_by(test_id=test_id) \
            .first()
        return service.test_db_to_test(test_db)

    def add_test(self, test: Test) -> bool:
        try:
            new_test = TestsModel(
                course_id=test.course_id,
                content=test.content
            )
            self.session.add(new_test)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления теста в БД " + str(e))

    def update_test(self, test: Test) -> bool:
        try:
            test_to_update = self.get_test_by_id(test_id=test.test_id)
            test_to_update.course_id = test.course_id
            test_to_update.content = test.content
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления теста в БД " + str(e))
