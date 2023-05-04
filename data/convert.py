from typing import Type

from data.types import *
from data.models import *


def user_db_to_user(user: UsersModel) -> User:
    return User(user_id=user.user_id,
                email=user.email,
                username=user.username,
                city=user.city,
                avatar=user.avatar,
                password=user.password)


def user_to_users_db(user: User) -> UsersModel:
    return UsersModel(
        email=user.email,
        city=user.city,
        username=user.username,
        password=user.password
    )


def achievement_db_to_achievemnt(achievement: Type[AchievementsModel]) -> Achievement:
    return Achievement(ach_id=achievement.ach_id,
                       course_id=achievement.course_id,
                       name=achievement.name,
                       image=achievement.image)


def ach_rel_db_to_ach_rel(ach_rel: Type[AchieveRelModel]) -> AchieveRel:
    return AchieveRel(ach_rel_id=ach_rel.ach_rel_id,
                      ach_id=ach_rel.ach_id,
                      user_id=ach_rel.user_id)


def course_db_to_course(course_db: Type[CoursesModel]) -> Course:
    return Course(course_id=course_db.course_id,
                  name=course_db.name,
                  avatar=course_db.avatar)


def course_rel_db_to_course_rel(course_rel_db: Type[CoursesRelModel]):
    return CourseRel(cour_rel_id=course_rel_db.cour_rel_id,
                     user_id=course_rel_db.user_id,
                     course_id=course_rel_db.course_id)


def curator_db_to_curator(curator_db: Type[CuratorsModel]):
    return Curator(cur_id=curator_db.cur_id,
                   user_id=curator_db.user_id,
                   course_id=curator_db.course_id)


def review_db_to_review(review_db: Type[ReviewsModel]):
    return Review(rev_id=review_db.rev_id,
                  user_id=review_db.user_id,
                  course_id=review_db.course_id,
                  rate=review_db.rate,
                  text=review_db.text)


def task_db_to_task(task_db: Type[TasksModel]):
    return Task(task_id=task_db.task_id,
                user_id=task_db.user_id,
                name=task_db.name,
                tags=task_db.tags,
                description=task_db.description,
                _date=task_db.date,
                completed=task_db.completed)


def sub_db_to_sub(sub: Type[SubRelModel]):
    return SubRel(sub_rel_id=sub.sub_rel_id,
                  user_id=sub.user_id,
                  sub_id=sub.sub_id)


def test_db_to_test(test_db: Type[TestsModel]):
    test = Test(test_id=test_db.test_id, course_id=test_db.course_id, content=None)
    test.content = TestContent.from_json(test_db.content)
    return test

