from flask import url_for
from data.repositories import *
from logic.auth.check import am_i_subscriber_of


class DataFacade:

    def __init__(self, session):
        self.user_repository = UserRepository(session)
        self.achievement_repository = AchievementRepository(session)
        self.achieve_rel_repository = AchieveRelRepository(session)
        self.course_repository = CourseRepository(session)
        self.course_rel_repository = CourseRelRepository(session)
        self.curator_repository = CuratorRepository(session)
        self.review_repository = ReviewRepository(session)
        self.task_repository = TaskRepository(session)
        self.sub_rel_repository = SubRelRepository(session)
        self.test_repository = TestRepository(session)
        self.articles_repository = ArticlesRepository(session)
        self.user_progress_repository = UserProgressRepository(session)
        self.role_repository = RoleRepository(session)
        self.chat_repository = ChatRepository(session)
        self.chat_messages_repository = ChatMessageRepository(session)

    def __get_user_achievements(self, user_id: int) -> Optional[list]:
        user_achievements_list = []
        ach_rel_list = self.achieve_rel_repository.get_achive_rels_by_user_id(user_id)
        if ach_rel_list is not None:
            for ach_rel in ach_rel_list:
                achievement = self.achievement_repository.get_achievement_by_id(ach_rel.ach_id)
                user_achievements_list.append(achievement)
            return user_achievements_list
        return None

    def __get_user_courses(self, user_id: int) -> Optional[list]:
        user_courses = []
        course_rel_list = self.course_rel_repository.get_course_rels_by_user_id(user_id)
        if course_rel_list is not None:
            for course_rel in course_rel_list:
                course = self.course_repository.get_course_by_course_id(course_rel.course_id)
                user_courses.append(course)
            return user_courses
        return None

    def __get_user_subs(self, user_id: int) -> Optional[list]:
        user_subs = []
        subs_rel_list = self.sub_rel_repository.get_all_by_user_id(user_id)
        if subs_rel_list is not None:
            for sub_rel in subs_rel_list:
                sub = self.user_repository.get_user_by_id(sub_rel.sub_id)
                user_subs.append(sub)
            return user_subs
        return None

    def __get_user_sub_to(self, user_id: int) -> Optional[list]:
        user_sub_to = []
        sub_to_list = self.sub_rel_repository.get_all_by_sub_id(user_id)
        if sub_to_list is not None:
            for sub_rel in sub_to_list:
                sub_to = self.user_repository.get_user_by_id(sub_rel.user_id)
                user_sub_to.append(sub_to)
            return user_sub_to
        return None

    def get_users_by_query(self, query: str) -> Optional[list]:
        users_list = self.user_repository.get_users_by_substring(query)
        if users_list is not None:
            return users_list
        return None

    def get_user_avatar(self, app, user_id: int):
        img = None
        user = self.user_repository.get_user_by_id(user_id)
        if not user.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/default.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = user.avatar
        return img

    def get_user_for_profile(self, user_id, current_user_id):
        user = self.user_repository.get_user_by_id(user_id)
        user.achievements = self.__get_user_achievements(user_id)
        user.courses = self.__get_user_courses(user_id)
        user.subs = self.__get_user_subs(user.user_id)
        user.subs_count = len(user.subs) if user.subs else 0
        user.sub_to = self.__get_user_sub_to(user.user_id)
        user.sub_to_count = len(user.sub_to) if user.sub_to else 0

        # cur user
        cur_user = self.get_user_by_id(current_user_id)
        cur_user.sub_to = self.__get_user_sub_to(cur_user.user_id)

        need_subscribe = True
        is_me = False

        if cur_user.sub_to:
            if not am_i_subscriber_of(cur_user.sub_to, user):
                need_subscribe = True
            else:
                need_subscribe = False
        if user.user_id == cur_user.user_id:
            is_me = True

        user.is_me = is_me
        user.need_subscribe = need_subscribe
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def get_user_by_username(self, username):
        return self.user_repository.get_user_by_username(username)

    def get_user_for_subscriptions(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        user.sub_to = self.__get_user_sub_to(user_id)
        return user

    def add_test(self, test):
        return self.test_repository.add_test(test)

    def add_course(self, course):
        return self.course_repository.add_course(course)

    def update_course(self, course):
        return self.course_repository.update_course(course)

    def remove_course(self, course_id):
        return self.course_repository.remove_course(course_id)

    def get_test_by_id(self, test_id):
        return self.test_repository.get_test_by_id(test_id)

    def get_all_tests(self):
        return self.test_repository.get_all_tests()

    def get_last_test_by_course(self, course_id):
        return self.test_repository.get_last_test_by_course(course_id)

    def remove_test(self, test_id):
        return self.test_repository.remove_test(test_id)

    def update_test(self, test):
        return self.test_repository.update_test(test)

    def update_user(self, user):
        return self.user_repository.update_user(user)

    def upload_avatar(self, user):
        return self.user_repository.upload_avatar(user)

    def add_sub_rel(self, subrel):
        return self.sub_rel_repository.add_sub_rel(subrel)

    def get_user_for_courses(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        user_relations = self.course_rel_repository.get_course_rels_by_user_id(user_id)
        user_courses = []
        if user_relations is not None:
            for relation in user_relations:
                course = self.course_repository.get_course_by_course_id(relation.course_id)
                user_courses.append(course)
            user.courses = user_courses
            return user
        return user

    def course_get_avatar(self, app, course_id):
        img = None
        course = self.course_repository.get_course_by_course_id(course_id)
        if not course.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/nophoto.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено фото по умолчанию: " + str(e))
        else:
            img = course.avatar
        return img

    def course_get_courses_by_query(self, query):
        courses_list = self.course_repository.get_courses_by_substring(query)
        if courses_list is not None:
            return courses_list
        return None

    def course_get_by_id(self, course_id):
        return self.course_repository.get_course_by_course_id(course_id)

    def course_json_get_by_id(self, course_id):
        return self.course_repository.get_course_by_course_id_in_json(course_id)

    def get_last_course(self):
        return self.course_repository.get_last_course()

    def rel_add_course_rel(self, course_rel):
        return self.course_rel_repository.add_course_rel(course_rel)

    def get_course_rels_all(self, course_id):
        return self.course_rel_repository.get_course_rels_all(course_id)

    def rel_remove_course_rel(self, rel_id):
        return self.course_rel_repository.rel_remove_course_rel(rel_id)

    def article_get_by_id(self, article_id):
        return self.articles_repository.get_article_by_id(article_id)

    def article_get_all_by_course_id(self, course_id):
        return self.articles_repository.get_all_course_articles(course_id)

    def article_add_article(self, article):
        return self.articles_repository.add_article(article)

    def get_last_article_by_course(self, course_id):
        return self.articles_repository.get_last_article_by_course(course_id)

    def update_article(self, article):
        return self.articles_repository.update_article(article)

    def remove_article(self, article_id):
        return self.articles_repository.remove_article(article_id)

    def add_progress(self, user_progress):
        return self.user_progress_repository.add_progress(user_progress)

    def user_get_progress_by_course_user_ids(self, user_id, course_id):
        return self.user_progress_repository.get_progress_by_user_course_ids(user_id, course_id)

    def get_progress_by_id(self, progress_id):
        return self.user_progress_repository.get_progress_by_id(progress_id)

    def get_progress_by_user_course_ids_all(self, user_id, course_id):
        return self.user_progress_repository.get_progress_by_user_course_ids_all(user_id, course_id)

    def get_progress_by_course_id_all(self, course_id):
        return self.user_progress_repository.get_progress_by_course_id_all(course_id)

    def update_progress(self, progress):
        return self.user_progress_repository.update_progress(progress)

    def add_review(self, review):
        return self.review_repository.add_review(review)

    def get_reviews_by_course_id(self, course_id):
        return self.review_repository.get_reviews_by_course_id(course_id)

    def update_review(self, review):
        return self.review_repository.update_review(review)

    def role_get_user_roles_by_user_id(self, user_id):
        return self.role_repository.get_user_roles_by_id(user_id)

    def is_user_curator_of_course(self, user_id, course_id):
        return self.curator_repository.is_user_curator_of_course(user_id, course_id)

    def curator_add(self, user_id, course_id):
        return self.curator_repository.add_curator(Curator(user_id=user_id, course_id=course_id))

    def curator_remove(self, user_id, course_id):
        return self.curator_repository.remove_curator(user_id, course_id)

    def chat_get_user_chats_preview(self, user_id):
        chats = self.chat_repository.get_user_chats(user_id)
        previews = []
        if chats == None:
            return json.dumps({"chats": previews}, default=str, ensure_ascii=False)
        for chat in chats:
            last_msg = self.chat_messages_repository.get_last_chat_message_by_id(chat.chat_id)

            user_with = self.user_repository.get_user_by_id(chat.user_with)
            user_with_username = user_with.username
            user_with_id = user_with.user_id
            last_message = last_msg.msg_text
            from_user = self.user_repository.get_user_by_id(last_msg.msg_from).username
            time = last_msg.msg_date

            previews.append(ChatPreview(user_with_username, last_message, from_user, time, user_with_id, chat.checked, chat.chat_id).to_dict())
        return json.dumps({"chats": previews}, default=str, ensure_ascii=False)

    def chat_get_dialog(self, user_id, chat_id):
        is_user_chat = self.chat_repository.is_user_chat(user_id, chat_id)

        if not is_user_chat:
            return "not your chat"

        messages = self.chat_messages_repository.get_chat_messages_by_chat_id(chat_id)

        user_with = ''
        if messages is not None:
            user_with = [messages[0].msg_to, messages[0].msg_from]
            user_with.remove(user_id)
            user_with = self.user_repository.get_user_by_id(user_with[0])
        else:
            return ""

        msgs = []
        for message in messages:
            msg = message.to_dict()
            if msg['msg_from'] == user_id:
                msg['msg_from'] = "Я: "
            else:
                msg['msg_from'] = user_with.username + ": "
            msg.pop('msg_to')
            msgs.append(msg)

        # change status of dialog
        self.chat_repository.change_checked_status(chat_id, user_id, read=True)

        return json.dumps({"messages": msgs}, default=str, ensure_ascii=False)

    def chat_exists(self, user_from, user_to):
        return self.chat_repository.is_exist(user_from, user_to)

    def chat_change_check_status(self, chat_id, msg_to):
        return self.chat_repository.change_checked_status(chat_id, msg_to)
