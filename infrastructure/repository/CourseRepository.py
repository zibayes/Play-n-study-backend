import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import CoursesModel
from domain.Course import Course
from sqlalchemy.orm.session import Session


class CourseRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_course(self, course: Course) -> bool:
        try:
            new_course = CoursesModel(
                name=course.name
            )
            self.session.add(new_course)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления в БД " + str(e))
            return False

    def get_course_by_course_id(self, course_id: int) -> Optional[Course]:
        course_db = self.session.query(CoursesModel) \
            .filter_by(course_id=course_id) \
            .first()
        if course_db is not None:
            return service.course_db_to_course(course_db)
        return None
