import json

import sqlalchemy.exc
from data import convert as convert

from typing import Optional
from data.models import *
from data.types import *
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
            return convert.achievement_db_to_achievemnt(ach_db)
        return None


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
            ach_rel_list.append(convert.ach_rel_db_to_ach_rel(ach_rel))
        if len(ach_rel_list) > 0:
            return ach_rel_list
        return None


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
            courses_rel_list.append(convert.course_rel_db_to_course_rel(course_rel))
        if len(courses_rel_list) > 0:
            return courses_rel_list
        return None

    def get_one_by_user_and_course_ids(self, user_id, course_id):
        course_rel_id = self.session.query(CoursesRelModel) \
            .filter_by(course_id=course_id) \
            .filter_by(user_id=user_id) \
            .first()
        if course_rel_id is not None:
            return convert.course_rel_db_to_course_rel(course_rel_id)
        return None

    def rel_remove_course_rel(self, rel_id):
        try:
            self.session.query(CoursesRelModel) \
                .filter_by(cour_rel_id=rel_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления отношения sub_rel :" + str(e))
            return False


class CourseRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_course(self, course: Course) -> bool:
        try:
            new_course = CoursesModel(
                name=course.name,
                avatar=course.avatar,
                description=course.description,
                category=course.category,
                content=course.content
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
            return convert.course_db_to_course(course_db)
        return None

    def get_course_by_course_id_in_json(self, course_id: int) -> Optional[Course]:
        course_db = self.session.query(CoursesModel) \
            .filter_by(course_id=course_id) \
            .first()
        if course_db is not None:
            course_db.content = str(course_db.content).replace("'", '"')
            course_db.content = json.loads(course_db.content)
            return course_db
        return None

    def get_courses_by_substring(self, substring):
        courses_db = self.session.query(CoursesModel) \
            .filter(CoursesModel.name.like(substring + "%")) \
            .all()
        return convert.courses_db_to_courses(courses_db)


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
            curators_list.append(convert.curator_db_to_curator(curator))
        if len(curators_list) > 0:
            return curators_list
        return None


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
            reviews_list.append(convert.review_db_to_review(review))
        if len(reviews_list) > 0:
            return reviews_list
        return None


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
            subs_list.append(convert.sub_db_to_sub(sub))
        if len(subs_list) > 0:
            return subs_list
        return None

    def get_all_by_sub_id(self, sub_id) -> Optional[list]:
        sub_rel_db = self.session.query(SubRelModel) \
            .filter_by(sub_id=sub_id) \
            .all()
        sub_to_list = []
        for sub in sub_rel_db:
            sub_to_list.append(convert.sub_db_to_sub(sub))
        if len(sub_to_list) > 0:
            return sub_to_list
        return None

    def get_one_by_user_and_sub_ids(self, user_id, sub_id):
        sub_rel_db = self.session.query(SubRelModel) \
            .filter_by(user_id=user_id) \
            .filter_by(sub_id=sub_id) \
            .first()
        return convert.sub_db_to_sub(sub_rel_db)

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


class TaskRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_task(self, task: Task) -> bool:
        try:
            new_task = TasksModel(
                user_id=task.user_id,
                name=task.name,
                tags=task.tags,
                description=task.description,
                date=task.date,
                completed=False
            )
            self.session.add(new_task)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления в БД " + str(e))
            return False

    def get_tasks_by_user_id(self, user_id: int) -> Optional[list]:
        tasks_db = self.session.query(TasksModel) \
            .filter_by(user_id=user_id) \
            .all()
        tasks_list = []
        for task in tasks_db:
            tasks_list.append(convert.task_db_to_task(task))
        if len(tasks_list) > 0:
            return tasks_list
        return None


class TestRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def get_test_by_id(self, test_id):
        test_db = self.session.query(TestsModel) \
            .filter_by(test_id=test_id) \
            .first()
        return convert.test_db_to_test(test_db)

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
            test_to_update = self.session.query(TestsModel) \
                .filter_by(test_id=test.test_id) \
                .first()
            test_to_update.course_id = test.course_id
            test_to_update.content = test.content
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления теста в БД " + str(e))


class UserRepository:
    session: Session = None

    def __init__(self, session):
        self.session = session

    def add_user(self, user: User) -> bool:
        try:
            new_user = convert.user_to_users_db(user)
            self.session.add(new_user)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

    def update_user(self, user: User) -> bool:
        try:
            self.session.query(UsersModel) \
                .filter_by(user_id=user.user_id) \
                .update({'username': user.username,
                         'email': user.email,
                         'city': user.city,
                         'password': user.password})
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления в БД " + str(e))
            return False

    def upload_avatar(self, user: User) -> bool:
        try:
            self.session.query(UsersModel) \
                .filter_by(user_id=user.user_id) \
                .update({'avatar': user.avatar})
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления аватара в БД :" + str(e))
            return False

    def get_user_by_id(self, user_id) -> Optional[User]:
        user_db = self.session.query(UsersModel) \
            .filter_by(user_id=user_id) \
            .first()
        if user_db is not None:
            return convert.user_db_to_user(user_db)
        return None

    def get_user_by_username(self, username) -> Optional[User]:
        user_db = self.session.query(UsersModel) \
            .filter_by(username=username) \
            .first()
        if user_db is not None:
            return convert.user_db_to_user(user_db)
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_db = self.session.query(UsersModel) \
            .filter_by(email=email) \
            .first()
        if user_db is not None:
            return convert.user_db_to_user(user_db)
        return None

    def get_users_by_substring(self, substring: str) -> Optional[list]:
        users = []
        users_db = self.session.query(UsersModel) \
            .filter(UsersModel.username.like(substring + "%")) \
            .all()

        if users_db is not None:
            for user in users_db:
                users.append(convert.user_db_to_user(user))
        if len(users) > 0:
            return users
        return None


class ArticlesRepository:
    def __init__(self, session):
        self.session = session

    def add_article(self, article: Article):
        try:
            new_article = ArticlesModel(
                course_id=article.course_id,
                content=article.content
            )
            self.session.add(new_article)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления раздела в БД " + str(e))

    def get_article_by_id(self, article_id):
        article_db = self.session.query(ArticlesModel) \
            .filter_by(article_id=article_id) \
            .first()
        return convert.article_db_to_article(article_db)

    def get_all_course_articles(self, course_id):
        articles_db = self.session.query(ArticlesModel) \
            .filter_by(course_id=course_id)
        return convert.article_db_to_article(articles_db)


class UserProgressRepository:
    def __init__(self, session):
        self.session = session

    def get_progress_by_user_course_ids(self, user_id, course_id):
        progress_db = self.session.query(UsersProgressModel) \
            .filter_by(user_id=user_id, course_id=course_id) \
            .first()
        return convert.progress_db_to_progress(progress_db)

