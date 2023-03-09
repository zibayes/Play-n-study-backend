import sqlalchemy.exc

import infrastructure.repository.service as service

from typing import Optional
from presentation.models.models import ReviewsModel
from domain.Review import Review
from sqlalchemy.orm.session import Session


class ReviewRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_review(self, review: Review):
        try:
            new_review = ReviewsModel(
                user_id=review.user_id,
                course_id=review.course_id,
                rate=review.rate,
                text=review.text
            )
            self.session.add(new_review)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка при добавлении в БД " + str(e))
            return False

    def get_reviews_by_course_id(self, course_id: int) -> Optional[list]:
        reviews_db = self.session.query(ReviewsModel) \
            .filter_by(course_id=course_id) \
            .all()
        reviews_list = []
        for review in reviews_db:
            reviews_list.append(service.review_db_to_review(review))
        if len(reviews_list) > 0:
            return reviews_list
        return None
