import json

import sqlalchemy.exc
from data import convert as convert

from typing import Optional
from data.models import *
from data.types import *
from sqlalchemy.orm.session import Session
from sqlalchemy import desc, text


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

    def get_course_rels_all(self, course_id):
        courses_rels_db = self.session.query(CoursesRelModel) \
            .filter_by(course_id=course_id) \
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

    def update_course(self, course: Course) -> bool:
        try:
            course_to_update = self.session.query(CoursesModel) \
                .filter_by(course_id=course.course_id) \
                .first()
            course_to_update.name = course.name
            course_to_update.avatar = course.avatar
            course_to_update.description = course.description
            course_to_update.category = course.category
            course_to_update.content = CourseUnit.to_json(course.content)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления курса в БД " + str(e))
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
            return convert.course_db_to_course(course_db)
        return None

    def get_courses_by_substring(self, substring):
        courses_db = self.session.query(CoursesModel) \
            .filter(CoursesModel.name.ilike("%"+ substring + "%")) \
            .all()
        return convert.courses_db_to_courses(courses_db)

    def get_last_course(self):
        course_db = self.session.query(CoursesModel) \
            .order_by(CoursesModel.course_id.desc()) \
            .first()
        return convert.course_db_to_course(course_db)

    def remove_course(self, course_id) -> bool:
        try:
            self.session.query(CoursesModel) \
                .filter_by(course_id=course_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления курса :" + str(e))
            return False


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
            # curators_list.append(convert.curator_db_to_curator(curator))
            curators_list.append(curator)
        if len(curators_list) > 0:
            return curators_list
        return None

    def is_user_curator_of_course(self, user_id, course_id):
        curator_db = self.session.query(CuratorsModel) \
            .filter_by(user_id=user_id) \
            .filter_by(course_id=course_id) \
            .first()
        if curator_db:
            return True
        return False

    def remove_curator(self, user_id, course_id):
        try:
            self.session.query(CuratorsModel) \
                .filter_by(user_id=user_id) \
                .filter_by(course_id=course_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления из БД " + e)
            return False


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

    def update_review(self, review: Review) -> bool:
        try:
            review_to_update = self.session.query(ReviewsModel) \
                .filter_by(course_id=review.course_id, user_id=review.user_id) \
                .first()
            review_to_update.rate = review.rate
            review_to_update.text = review.text
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления отзыва в БД " + str(e))


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

    def get_all_tests(self):
        tests_db = self.session.query(TestsModel).all()
        return [convert.test_db_to_test(i) for i in tests_db]

    def get_test_by_id(self, test_id):
        test_db = self.session.query(TestsModel) \
            .filter_by(test_id=test_id) \
            .first()
        return convert.test_db_to_test(test_db)

    def get_last_test_by_course(self, course_id):
        test_db = self.session.query(TestsModel) \
            .filter_by(course_id=course_id) \
            .order_by(TestsModel.test_id.desc()) \
            .first()
        return convert.test_db_to_test(test_db)

    def add_test(self, test: Test) -> bool:
        try:
            new_test = TestsModel(
                course_id=test.course_id,
                unit_id=test.unit_id,
                avatar=test.avatar,
                description=test.description,
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
            test_to_update.unit_id = test.unit_id
            test_to_update.avatar = test.avatar
            test_to_update.description = test.description
            test_to_update.content = test.content
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления теста в БД " + str(e))

    def remove_test(self, test_id) -> bool:
        try:
            self.session.query(TestsModel) \
                .filter_by(test_id=test_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления теста :" + str(e))
            return False


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
            .filter(UsersModel.username.ilike(substring + "%")) \
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
                unit_id=article.unit_id,
                avatar=article.avatar,
                name=article.name,
                description=article.description,
                content=article.content,
                score=article.score
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

    def get_last_article_by_course(self, course_id):
        article_db = self.session.query(ArticlesModel) \
            .filter_by(course_id=course_id) \
            .order_by(ArticlesModel.article_id.desc()) \
            .first()
        return convert.article_db_to_article(article_db)

    def update_article(self, article: Article) -> bool:
        try:
            article_to_update = self.session.query(ArticlesModel) \
                .filter_by(article_id=article.article_id) \
                .first()
            article_to_update.course_id = article.course_id
            article_to_update.unit_id = article.unit_id
            article_to_update.avatar = article.avatar
            article_to_update.name = article.name
            article_to_update.description = article.description
            article_to_update.content = article.content
            article_to_update.score = article.score
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления статьи в БД " + str(e))
            return False

    def remove_article(self, article_id) -> bool:
        try:
            self.session.query(ArticlesModel) \
                .filter_by(article_id=article_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления статьи :" + str(e))
            return False


class UserProgressRepository:
    def __init__(self, session):
        self.session = session

    def get_progress_by_user_course_ids(self, user_id, course_id):
        progress_db = self.session.query(UsersProgressModel) \
            .filter_by(user_id=user_id, course_id=course_id) \
            .first()
        return convert.progress_db_to_progress(progress_db)

    def get_progress_by_user_course_ids_all(self, user_id, course_id):
        progresses_db = self.session.query(UsersProgressModel) \
            .filter_by(user_id=user_id, course_id=course_id) \
            .all()
        for i in range(len(progresses_db)):
            progresses_db[i] = convert.progress_db_to_progress(progresses_db[i])
        return progresses_db

    def get_progress_by_id(self, progress_id):
        progress_db = self.session.query(UsersProgressModel) \
            .filter_by(up_id=progress_id) \
            .first()
        return convert.progress_db_to_progress(progress_db)

    def get_progress_by_course_id_all(self, course_id):
        progresses_db = self.session.query(UsersProgressModel) \
            .filter_by(course_id=course_id) \
            .all()
        for i in range(len(progresses_db)):
            progresses_db[i] = convert.progress_db_to_progress(progresses_db[i])
        return progresses_db

    def add_progress(self, user_progress):
        try:
            new_user_progress = UsersProgressModel(
                user_id=user_progress.user_id,
                course_id=user_progress.course_id,
                task_type=user_progress.task_type,
                task_id=user_progress.task_id,
                progress=user_progress.progress
            )
            self.session.add(new_user_progress)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления прогресса в БД " + str(e))

    def remove_progress(self, up_id) -> bool:
        try:
            self.session.query(UsersProgressModel) \
                .filter_by(up_id=up_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления пользовательского прогресса :" + str(e))
            return False

    def update_progress(self, user_progress):
        try:
            progress_to_update = self.session.query(UsersProgressModel) \
                .filter_by(up_id=user_progress.up_id) \
                .first()
            progress_to_update.progress = user_progress.progress
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления прогресса в БД " + str(e))
            return False

    def get_last_progress_by_task(self, user_id, course_id, task_id, task_type):
        progress_db = self.session.query(UsersProgressModel) \
            .filter_by(user_id=user_id, course_id=course_id, task_id=task_id, task_type=task_type)\
            .order_by(UsersProgressModel.up_id.desc()) \
            .first()
        return convert.progress_db_to_progress(progress_db)


class RoleRepository:
    def __init__(self, session):
        self.session = session

    def get_user_roles_by_id(self, user_id):
        relations = self.session.query(UsersRolesModel) \
            .filter_by(user_id=user_id) \
            .all()
        if relations:
            roles = []
            for relation in relations:
                role = self.session.query(RolesModel) \
                          .filter_by(role_id=relation.role_id) \
                          .first()
                if role:
                    roles.append(role.name.lower())
            return roles
        else:
            return None

    def add_user_role_admin(self, user_id):
        try:
            new_user_role = UsersRolesModel(
                user_id=user_id,
                role_id=1,
            )
            self.session.add(new_user_role)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления роли админа " + str(e))

    def remove_user_role_admin(self, user_id) -> bool:
        try:
            self.session.query(UsersRolesModel) \
                .filter_by(user_id=user_id, role_id=1) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления роли админа :" + str(e))
            return False


class MessagesRepository:
    def __init__(self, session):
        self.session = session

    def get_chat_messages(self, chat_id):
        messages = self.session.query(ChatMessagesModel) \
            .filter_by(chat_id=chat_id) \
            .all()
        msgs = []
        for message in messages:
            msgs.append(convert.msg_db_to_msg(message))
        return msgs


class ChatRepository:
    def __init__(self, session):
        self.session = session

    def get_user_chats(self, user_id):
        chats = self.session.query(ChatsModel) \
            .filter_by(user1=user_id) \
            .all()
        chats1 = self.session.query(ChatsModel) \
            .filter_by(user2=user_id) \
            .all()
        chats += chats1

        if len(chats) == 0:
            return None

        chats = sorted(chats, key=lambda x: x.last_change)

        normalized_chats = []
        for chat in chats:
            ids = [chat.user1, chat.user2]
            ids.remove(user_id)
            unread = self.__is_unread_by_me(user_id, chat.chat_id)

            normalized_chats.append(Chat(chat.chat_id, ids[0], chat.last_change, unread))
        return normalized_chats

    def is_exist(self, user_from, user_to):
        chat = self.session.query(ChatsModel) \
            .filter_by(user1=user_from) \
            .filter_by(user2=user_to) \
            .all()
        if len(chat) > 0:
            return True
        chat = self.session.query(ChatsModel) \
            .filter_by(user1=user_to) \
            .filter_by(user2=user_from) \
            .all()
        if len(chat) > 0:
            return True
        return False

    def get_chat_id(self, user1, user2):
        chat = self.session.query(ChatsModel) \
            .filter_by(user1=user1) \
            .filter_by(user2=user2) \
            .first()
        if chat is not None:
            return chat.chat_id
        chat = self.session.query(ChatsModel) \
            .filter_by(user1=user2) \
            .filter_by(user2=user1) \
            .first()
        if chat is not None:
            return chat.chat_id
        return None

    def create(self, user_from, user_to):
        try:
            new_chat = ChatsModel(
                user1=user_from,
                user2=user_to
            )
            self.session.add(new_chat)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Error: " + str(e))
            return False

    def __is_unread_by_me(self, user_id, chat_id):
        chat = self.session.query(ChatsModel) \
            .filter_by(chat_id=chat_id) \
            .first()
        if chat is None:
            return None

        if chat.user1 == user_id:
            return chat.user1_read

        return chat.user2_read

    def change_checked_status(self, chat_id, user_id, read=False):
        chat = self.session.query(ChatsModel) \
            .filter_by(chat_id=chat_id) \
            .first()

        if chat is None:
            return False

        msgs = self.session.query(ChatMessagesModel) \
            .filter_by(chat_id=chat_id) \
            .order_by(text("msg_date desc")) \
            .all()

        status = True

        if not read:
            status = False

        for msg in msgs:
            msg.user_to_read = status

        if chat.user1 == user_id:
            chat.user1_read = status
        else:
            chat.user2_read = status
        self.session.commit()
        return True

    def is_user_chat(self, user_id, chat_id):
        chat = self.session.query(ChatsModel) \
                    .filter_by(chat_id=chat_id) \
                    .first()
        if chat is None:
            return None

        if chat.user1 == user_id:
            return True
        if chat.user2 == user_id:
            return True
        return False

    def remove_chat(self, chat_id) -> bool:
        try:
            self.session.query(ChatsModel) \
                .filter_by(chat_id=chat_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления чата :" + str(e))
            return False


class ChatMessageRepository:
    def __init__(self, session):
        self.session = session

    def get_last_chat_message_by_id(self, chat_id):
        message = self.session.query(ChatMessagesModel) \
            .filter_by(chat_id=chat_id) \
            .order_by(text("msg_date desc")) \
            .first()
        if message is not None:
            return convert.msg_db_to_msg(message)
        return None

    def get_chat_messages_by_chat_id(self, chat_id):
        messages = self.session.query(ChatMessagesModel) \
            .filter_by(chat_id=chat_id) \
            .order_by(text("msg_date")) \
            .all()
        if len(messages) > 0:
            return list(map(lambda x: convert.msg_db_to_msg(x), messages))
        return None

    def send_message(self, message):
        try:
            new_message = ChatMessagesModel(
                chat_id=message.chat_id,
                msg_text=message.msg_text,
                msg_date=func.now(),
                msg_from=message.msg_from,
                msg_to=message.msg_to,
                user_to_read=message.user_to_read)

            self.session.add(new_message)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Error " + str(e))
            return False

    def remove_message(self, msg_id) -> bool:
        try:
            self.session.query(ChatMessagesModel) \
                .filter_by(msg_id=msg_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления сообщения :" + str(e))
            return False


class LinksRepository:
    def __init__(self, session):
        self.session = session

    def add_link(self, link: Link):
        try:
            new_link = LinksModel(
                course_id=link.course_id,
                unit_id=link.unit_id,
                avatar=link.avatar,
                name=link.name,
                link=link.link
            )
            self.session.add(new_link)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления раздела в БД " + str(e))

    def get_link_by_id(self, link_id):
        link_db = self.session.query(LinksModel) \
            .filter_by(link_id=link_id) \
            .first()
        return convert.link_db_to_link(link_db)

    def get_all_course_links(self, course_id):
        links_db = self.session.query(LinksModel) \
            .filter_by(course_id=course_id)
        return convert.link_db_to_link(links_db)

    def get_last_link_by_course(self, course_id):
        link_db = self.session.query(LinksModel) \
            .filter_by(course_id=course_id) \
            .order_by(LinksModel.link_id.desc()) \
            .first()
        return convert.link_db_to_link(link_db)

    def update_link(self, link: Link) -> bool:
        try:
            link_to_update = self.session.query(LinksModel) \
                .filter_by(link_id=link.link_id) \
                .first()
            link_to_update.course_id = link.course_id
            link_to_update.unit_id = link.unit_id
            link_to_update.avatar = link.avatar
            link_to_update.name = link.name
            link_to_update.link = link.link
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления ссылки в БД " + str(e))
            return False

    def remove_link(self, link_id) -> bool:
        try:
            self.session.query(LinksModel) \
                .filter_by(link_id=link_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления ссылки :" + str(e))
            return False



class ForumsRepository:
    def __init__(self, session):
        self.session = session

    def add_forum(self, forum: Forum):
        try:
            new_forum = ForumsModel(
                course_id=forum.course_id,
                unit_id=forum.unit_id,
                avatar=forum.avatar,
                name=forum.name,
                description=forum.description
            )
            self.session.add(new_forum)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления форума в БД " + str(e))

    def get_forum_by_id(self, forum_id):
        forum_db = self.session.query(ForumsModel) \
            .filter_by(forum_id=forum_id) \
            .first()
        return convert.forum_db_to_forum(forum_db)

    def get_all_course_forums(self, course_id):
        forums_db = self.session.query(ForumsModel) \
            .filter_by(course_id=course_id)
        return convert.forum_db_to_forum(forum_db)

    def get_last_forum_by_course(self, course_id):
        forum_db = self.session.query(ForumsModel) \
            .filter_by(course_id=course_id) \
            .order_by(ForumsModel.forum_id.desc()) \
            .first()
        return convert.forum_db_to_forum(forum_db)

    def update_forum(self, forum: Forum) -> bool:
        try:
            forum_to_update = self.session.query(ForumsModel) \
                .filter_by(forum_id=forum.forum_id) \
                .first()
            forum_to_update.course_id = forum.course_id
            forum_to_update.unit_id = forum.unit_id
            forum_to_update.avatar = forum.avatar
            forum_to_update.name = forum.name
            forum_to_update.description = forum.description
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления форума в БД " + str(e))
            return False

    def remove_forum(self, forum_id) -> bool:
        try:
            self.session.query(ForumsModel) \
                .filter_by(forum_id=forum_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления форума:" + str(e))
            return False


class ForumTopicsRepository:
    def __init__(self, session):
        self.session = session

    def add_forum_topic(self, forum_topic: ForumTopic):
        try:
            new_forum_topic = ForumTopicsModel(
                forum_id=forum_topic.forum_id,
                name=forum_topic.name,
            )
            self.session.add(new_forum_topic)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления темы форума в БД " + str(e))

    def get_forum_topic_by_id(self, ft_id):
        forum_topic_db = self.session.query(ForumTopicsModel) \
            .filter_by(ft_id=ft_id) \
            .first()
        return convert.forum_topic_db_to_forum_topic(forum_topic_db)

    def get_all_forum_topics(self, forum_id):
        forum_topic_db = self.session.query(ForumTopicsModel) \
            .filter_by(forum_id=forum_id)
        return convert.forum_topic_db_to_forum_topic(forum_topic_db)

    def get_last_topic_by_forum(self, forum_id):
        forum_topic_db = self.session.query(ForumTopicsModel) \
            .filter_by(forum_id=forum_id) \
            .order_by(ForumTopicsModel.ft_id.desc()) \
            .first()
        return convert.forum_topic_db_to_forum_topic(forum_topic_db)

    def update_forum_topic(self, forum_topic: ForumTopic) -> bool:
        try:
            forum_topic_to_update = self.session.query(ForumTopicsModel) \
                .filter_by(ft_id=forum_topic.ft_id) \
                .first()
            forum_topic_to_update.forum_id = forum_topic.forum_id
            forum_topic_to_update.name = forum_topic.name
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления темы форума в БД " + str(e))
            return False

    def remove_forum_topic(self, ft_id) -> bool:
        try:
            self.session.query(ForumTopicsModel) \
                .filter_by(ft_id=ft_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления темы форума:" + str(e))
            return False


class TopicMessagesRepository:
    def __init__(self, session):
        self.session = session

    def add_message(self, topic_message: TopicMessage):
        try:
            new_topic_message = TopicMessagesModel(
                ft_id=topic_message.ft_id,
                parent_tm_id=topic_message.parent_tm_id,
                user_id=topic_message.user_id,
                tm_date=topic_message.tm_date,
                content=topic_message.content,
            )
            self.session.add(new_topic_message)
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка добавления сообщения форума в БД " + str(e))

    def get_message_by_id(self, tm_id):
        topic_message_db = self.session.query(TopicMessagesModel) \
            .filter_by(tm_id=tm_id) \
            .first()
        return convert.topic_message_db_to_topic_message(topic_message_db)

    def get_all_topic_messages(self, ft_id):
        topic_message_db = self.session.query(TopicMessagesModel) \
            .filter_by(ft_id=ft_id)
        return convert.topic_message_db_to_topic_message(topic_message_db)

    def get_last_message_by_topic(self, ft_id):
        topic_message_db = self.session.query(TopicMessagesModel) \
            .filter_by(ft_id=ft_id) \
            .order_by(TopicMessagesModel.tm_id.desc()) \
            .first()
        return convert.topic_message_db_to_topic_message(topic_message_db)

    def update_message(self, topic_message: TopicMessage) -> bool:
        try:
            topic_message_to_update = self.session.query(TopicMessagesModel) \
                .filter_by(tm_id=topic_message.tm_id) \
                .first()
            topic_message_to_update.ft_id = forum_topic.ft_id
            topic_message_to_update.parent_tm_id = forum_topic.parent_tm_id
            topic_message_to_update.user_id = forum_topic.user_id
            topic_message_to_update.tm_date = forum_topic.tm_date
            topic_message_to_update.content = forum_topic.content
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка обновления сообщения форума в БД " + str(e))
            return False

    def remove_message(self, tm_id) -> bool:
        try:
            self.session.query(TopicMessagesModel) \
                .filter_by(tm_id=tm_id) \
                .delete()
            self.session.commit()
            return True
        except sqlalchemy.exc.DatabaseError as e:
            print("Ошибка удаления сообщения форума:" + str(e))
            return False