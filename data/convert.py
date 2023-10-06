import json
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
    course_db.content = str(course_db.content).replace("'", '"')
    return Course(course_id=course_db.course_id,
                  name=course_db.name,
                  avatar=course_db.avatar,
                  description=course_db.description,
                  category=course_db.category,
                  content=CourseUnit.from_json(json.loads(course_db.content)))


def course_to_course_db(course: Course) -> CoursesModel:
    return CoursesModel(
        name=course.name,
        avatar=course.avatar,
        description=course.description,
        category=course.category,
        content=CourseUnit.to_json(course.content)
    )


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
    test = Test(test_id=test_db.test_id, course_id=test_db.course_id, unit_id=test_db.unit_id, content=None, avatar=test_db.avatar, description=test_db.description)
    test.content = TestContent.from_json(test_db.content)
    return test


def courses_db_to_courses(courses):
    crs = []
    for cour in courses:
        crs.append(course_db_to_course(cour))
    return crs if len(crs) > 0 else None


def article_db_to_article(article: Type[ArticlesModel]):
    return Article(article_id=article.article_id,
                   course_id=article.course_id,
                   avatar=article.avatar,
                   description=article.description,
                   unit_id=article.unit_id,
                   content=article.content)


def progress_db_to_progress(progress: Type[UsersProgressModel]):
    return UserProgress(up_id=progress.up_id,
                        user_id=progress.user_id,
                        course_id=progress.course_id,
                        task_id=progress.task_id,
                        task_type=progress.task_type,
                        progress=Progress.from_json(json.loads(progress.progress)))


def msg_db_to_msg(message):
    return ChatMessage(msg_id=message.msg_id,
                       chat_id=message.chat_id,
                       msg_text=message.msg_text,
                       msg_date=message.msg_date,
                       msg_from=message.msg_from,
                       msg_to=message.msg_to)


def message_db_to_message(x):
    return None


def link_db_to_link(link: Type[LinksModel]):
    return Link(link_id=link.link_id,
                   course_id=link.course_id,
                   avatar=link.avatar,
                   name=link.name,
                   unit_id=link.unit_id,
                   link=link.link)