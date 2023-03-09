from presentation.models.models import *
from typing import Optional
from infrastructure.repository.UserRepository import UserRepository
from infrastructure.repository.AchievementRepository import AchievementRepository
from infrastructure.repository.AchieveRelRepository import AchieveRelRepository
from infrastructure.repository.CourseRepository import CourseRepository
from infrastructure.repository.CourseRelRepository import CourseRelRepository
from infrastructure.repository.CuratorRepository import CuratorRepository
from infrastructure.repository.ReviewRepository import ReviewRepository
from infrastructure.repository.TaskRepository import TaskRepository


class QueryManager:
    user_repository: UserRepository = None
    achievement_repository: AchievementRepository = None
    achieve_rel_repository: AchieveRelRepository = None
    course_repository: CourseRepository = None
    course_rel_repository: CourseRelRepository = None
    curator_repository: CuratorRepository = None
    review_repository: ReviewRepository = None
    task_repository: TaskRepository = None

    def __init__(self, user_repository: UserRepository,
                 achievement_repository: AchievementRepository,
                 achieve_rel_repository: AchieveRelRepository,
                 course_repository: CourseRepository,
                 course_rel_repository: CourseRelRepository,
                 curator_repository: CuratorRepository,
                 review_repository: ReviewRepository,
                 task_repository: TaskRepository
                 ):
        self.user_repository = user_repository
        self.achievement_repository = achievement_repository
        self.achieve_rel_repository = achieve_rel_repository
        self.course_repository = course_repository
        self.course_rel_repository = course_rel_repository
        self.curator_repository = curator_repository
        self.review_repository = review_repository
        self.task_repository = task_repository

    def get_user_achievements(self, user_id: int) -> Optional[list]:
        user_achievements_list = []
        ach_rel_list = self.achieve_rel_repository.get_achive_rels_by_user_id(user_id)
        if ach_rel_list is not None:
            for ach_rel in ach_rel_list:
                achievement = self.achievement_repository.get_achievement_by_id(ach_rel.ach_id)
                user_achievements_list.append(achievement)
            return user_achievements_list
        return None

    def get_user_courses(self, user_id: int) -> Optional[list]:
        user_courses = []
        course_rel_list = self.course_rel_repository.get_course_rels_by_user_id(user_id)
        if course_rel_list is not None:
            for course_rel in course_rel_list:
                course = self.course_repository.get_course_by_course_id(course_rel.course_id)
                user_courses.append(course)
            return user_courses
        return None

