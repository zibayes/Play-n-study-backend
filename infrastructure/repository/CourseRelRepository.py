import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import CoursesRelModel
from domain.CourseRel import CourseRel
from sqlalchemy.orm.session import Session


class CourseRelRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_course_rel(self, course_rel: CourseRel) -> bool:
        try:
            new_course_rel = CoursesRelModel(
                user_id=course_rel.user_id,
                course_id=course_rel.course_id
            )
            self.session.add(new_course_rel)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка при добавленеии в БД " + str(e))
            return False

    def get_course_rels_by_user_id(self, user_id):
        courses_rels_db = self.session.query(CoursesRelModel) \
            .filter_by(user_id=user_id) \
            .all()
        courses_rel_list = []
        for course_rel in courses_rels_db:
            courses_rel_list.append(service.course_rel_db_to_course_rel(course_rel))
        if len(courses_rel_list) > 0:
            return courses_rel_list
        return None
