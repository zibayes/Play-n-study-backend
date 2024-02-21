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
        self.links_repository = LinksRepository(session)
        self.forums_repository = ForumsRepository(session)
        self.forum_topics_repository = ForumTopicsRepository(session)
        self.topic_messages_repository = TopicMessagesRepository(session)
        self.user_progress_repository = UserProgressRepository(session)
        self.role_repository = RoleRepository(session)
        self.chat_repository = ChatRepository(session)
        self.chat_messages_repository = ChatMessageRepository(session)
        self.notifications_repository = NotificationsRepository(session)
        self.notes_repository = NotesRepository(session)

    def get_user_achievements(self, user_id: int) -> Optional[list]:
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
        user.achievements = self.get_user_achievements(user_id)
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

        user.notifications = self.get_all_notifications_by_user_id(user_id)
        if user.notifications:
            for notif in user.notifications:
                if not notif.user_to_read:
                    user.notifications_count += 1
        return user

    def get_user_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        user.notifications = self.get_all_notifications_by_user_id(user_id)
        if user.notifications:
            for notif in user.notifications:
                if not notif.user_to_read:
                    user.notifications_count += 1
        return user

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
        user.notifications = self.get_all_notifications_by_user_id(user_id)
        if user.notifications:
            for notif in user.notifications:
                if not notif.user_to_read:
                    user.notifications_count += 1
        user_courses = []
        if user_relations is not None:
            for relation in user_relations:
                course = self.course_repository.get_course_by_course_id(relation.course_id)
                user_courses.append(course)
            user.courses = user_courses
            return user
        return user

    def forum_get_avatar(self, app, forum_id):
        img = None
        forum = self.forums_repository.get_forum_by_id(forum_id)
        if not forum.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/nophoto.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено фото по умолчанию: " + str(e))
        else:
            img = forum.avatar
        return img

    def link_get_avatar(self, app, link_id):
        img = None
        link = self.links_repository.get_link_by_id(link_id)
        if not link.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/nophoto.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено фото по умолчанию: " + str(e))
        else:
            img = link.avatar
        return img

    def article_get_avatar(self, app, article_id):
        img = None
        article = self.articles_repository.get_article_by_id(article_id)
        if not article.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/nophoto.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено фото по умолчанию: " + str(e))
        else:
            img = article.avatar
        return img

    def test_get_avatar(self, app, test_id):
        img = None
        test = self.test_repository.get_test_by_id(test_id)
        if not test.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/nophoto.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено фото по умолчанию: " + str(e))
        else:
            img = test.avatar
        return img

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

    def add_achieve_rel(self, achieve_rel):
        self.achieve_rel_repository.add_achieve_rel(achieve_rel)

    def achive_rel_exist(self, ach_id, user_id):
        return self.achieve_rel_repository.achive_rel_exist(ach_id, user_id)

    def get_achive_rels_by_achievement_id(self, ach_id):
        return self.achieve_rel_repository.get_achive_rels_by_achievement_id(ach_id)

    def remove_achive_rel(self, ach_rel_id):
        return self.achieve_rel_repository.remove_achive_rel(ach_rel_id)

    def add_achievement(self, achievement: Achievement):
        return self.achievement_repository.add_achievement(achievement)

    def get_achievement_by_id(self, ach_id):
        return self.achievement_repository.get_achievement_by_id(ach_id)

    def get_achievements_by_course_id(self, course_id):
        return self.achievement_repository.get_achievements_by_course_id(course_id)

    def update_achievement(self, achievement):
        return self.achievement_repository.update_achievement(achievement)

    def remove_achievement(self, ach_id):
        return self.achievement_repository.remove_achievement(ach_id)

    def achievement_get_avatar(self, app, ach_id):
        img = None
        achievement = self.achievement_repository.get_achievement_by_id(ach_id)
        if not achievement.image:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="img/nophoto.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найдено фото по умолчанию: " + str(e))
        else:
            img = achievement.image
        return img

    def get_last_article_by_course(self, course_id):
        return self.articles_repository.get_last_article_by_course(course_id)

    def update_article(self, article):
        return self.articles_repository.update_article(article)

    def remove_article(self, article_id):
        return self.articles_repository.remove_article(article_id)

    def link_get_by_id(self, link_id):
        return self.links_repository.get_link_by_id(link_id)

    def link_get_all_by_course_id(self, course_id):
        return self.links_repository.get_all_course_links(course_id)

    def link_add_link(self, link):
        return self.links_repository.add_link(link)

    def get_last_link_by_course(self, link_id):
        return self.links_repository.get_last_link_by_course(link_id)

    def update_link(self, link):
        return self.links_repository.update_link(link)

    def remove_link(self, link_id):
        return self.links_repository.remove_link(link_id)

    def get_forum_by_id(self, forum_id):
        return self.forums_repository.get_forum_by_id(forum_id)

    def forum_get_all_by_course_id(self, course_id):
        return self.forums_repository.get_all_course_forums(course_id)

    def forum_add_forum(self, forum):
        return self.forums_repository.add_forum(forum)

    def get_last_forum_by_course(self, forum_id):
        return self.forums_repository.get_last_forum_by_course(forum_id)

    def update_forum(self, forum):
        return self.forums_repository.update_forum(forum)

    def remove_forum(self, forum_id):
        return self.forums_repository.remove_forum(forum_id)

    def forum_topic_get_by_id(self, ft_id):
        return self.forum_topics_repository.get_forum_topic_by_id(ft_id)

    def topic_get_all_by_forum_id(self, forum_id):
        return self.forum_topics_repository.get_all_forum_topics(forum_id)

    def forum_topic_add_forum_topic(self, forum_topic):
        return self.forum_topics_repository.add_forum_topic(forum_topic)

    def get_last_topic_by_forum(self, forum_id):
        return self.forum_topics_repository.get_last_topic_by_forum(forum_id)

    def update_forum_topic(self, forum_topic):
        return self.forum_topics_repository.update_forum_topic(forum_topic)

    def remove_forum_topic(self, ft_id):
        return self.forum_topics_repository.remove_forum_topic(ft_id)

    def get_topics_by_query(self, query: str, forum_id: int) -> Optional[list]:
        topics_list = self.forum_topics_repository.get_forum_topics_by_substring(query, forum_id)
        if topics_list is not None:
            return topics_list
        return None

    def topic_message_get_by_id(self, tm_id):
        return self.topic_messages_repository.get_message_by_id(tm_id)

    def messages_get_all_by_topic_id(self, ft_id):
        return self.topic_messages_repository.get_all_topic_messages(ft_id)

    def add_topic_message(self, topic_message):
        return self.topic_messages_repository.add_message(topic_message)

    def get_last_message_by_topic(self, ft_id):
        return self.topic_messages_repository.get_last_message_by_topic(ft_id)

    def update_topic_message(self, topic_message):
        return self.topic_messages_repository.update_message(topic_message)

    def remove_topic_message(self, tm_id):
        return self.topic_messages_repository.remove_message(tm_id)

    def add_progress(self, user_progress):
        return self.user_progress_repository.add_progress(user_progress)

    def remove_progress(self, up_id):
        return self.user_progress_repository.remove_progress(up_id)

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

    def get_last_progress_by_task(self, user_id, course_id, task_id, task_type):
        return self.user_progress_repository.get_last_progress_by_task(user_id, course_id, task_id, task_type)

    def add_review(self, review):
        return self.review_repository.add_review(review)

    def get_reviews_by_course_id(self, course_id):
        return self.review_repository.get_reviews_by_course_id(course_id)

    def update_review(self, review):
        return self.review_repository.update_review(review)

    def role_get_user_roles_by_user_id(self, user_id):
        return self.role_repository.get_user_roles_by_id(user_id)

    def add_user_role_admin(self, user_id):
        return self.role_repository.add_user_role_admin(user_id)

    def remove_user_role_admin(self, user_id):
        return self.role_repository.remove_user_role_admin(user_id)

    def is_user_curator_of_course(self, user_id, course_id):
        return self.curator_repository.is_user_curator_of_course(user_id, course_id)

    def get_curators_by_course_id(self, course_id):
        return self.curator_repository.get_curators_by_course_id(course_id)

    def curator_add(self, user_id, course_id):
        return self.curator_repository.add_curator(Curator(user_id=user_id, course_id=course_id))

    def curator_remove(self, user_id, course_id):
        return self.curator_repository.remove_curator(user_id, course_id)

    def chats_start_dialog(self, current_user_id, user_id):
        return self.chat_repository.create(current_user_id, user_id)

    def remove_message(self, msg_id):
        return self.chat_messages_repository.remove_message(msg_id)

    def update_chat_message(self, message, msg_id):
        return self.chat_messages_repository.update_message(message, msg_id)

    def get_last_chat_message_by_id(self, chat_id):
        msg = self.chat_messages_repository.get_last_chat_message_by_id(chat_id).to_dict()
        msg['msg_from_id'] = self.user_repository.get_user_by_id(int(msg['msg_from'])).user_id
        msg['msg_from'] = "Я"
        return json.dumps(msg, default=str, ensure_ascii=False)

    def chat_get_user_chats_preview(self, user_id):
        chats = self.chat_repository.get_user_chats(user_id)
        previews = []
        current_user = self.get_user_by_id(user_id)
        if chats is None:
            return json.dumps({"chats": previews}, default=str, ensure_ascii=False)
        for chat in chats:
            last_msg = self.chat_messages_repository.get_last_chat_message_by_id(chat.chat_id)
            messages = self.chat_messages_repository.get_chat_messages_by_chat_id(chat.chat_id)
            msg_new_count = 0
            if messages:
                for msg in messages:
                    if not msg.user_to_read and msg.msg_to == current_user.user_id:
                        msg_new_count += 1

            user_with = self.user_repository.get_user_by_id(chat.user_with)
            user_with_username = user_with.username
            user_with_id = user_with.user_id
            from_user = self.user_repository.get_user_by_id(chat.user_with).username
            last_message = ''
            time = ''
            if last_msg:
                from_user = self.user_repository.get_user_by_id(last_msg.msg_from).username
                last_message = last_msg.msg_text
                time = last_msg.msg_date

            previews.append(ChatPreview(user_with_username, last_message, from_user, time, user_with_id, chat.checked, chat.chat_id, msg_new_count, current_user.user_id).to_dict())
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
                msg['msg_from'] = "Я"
                msg['msg_from_id'] = user_id
            else:
                msg['msg_from'] = user_with.username
                msg['msg_from_id'] = user_with.user_id
            msg.pop('msg_to')
            msgs.append(msg)

        # change status of dialog
        self.chat_repository.change_checked_status(chat_id, user_id, read=True)

        return json.dumps({"messages": msgs}, default=str, ensure_ascii=False)

    def chat_exists(self, user_from, user_to):
        return self.chat_repository.is_exist(user_from, user_to)

    def chat_change_check_status(self, chat_id, msg_to):
        return self.chat_repository.change_checked_status(chat_id, msg_to)

    def remove_chat(self, chat_id):
        messages = self.chat_messages_repository.get_chat_messages_by_chat_id(chat_id)
        for message in messages:
            self.remove_message(message.msg_id)
        return self.chat_repository.remove_chat(chat_id)

    def add_notification(self, notification):
        return self.notifications_repository.add_notification(notification)

    def get_notification_by_id(self, notif_id):
        return self.notifications_repository.get_notification_by_id(notif_id)

    def get_all_notifications_by_user_id(self, user_id):
        return self.notifications_repository.get_all_notifications_by_user_id(user_id)

    def remove_notification(self, notif_id):
        return self.notifications_repository.remove_notification(notif_id)

    def remove_all_notifications_by_user_id(self, user_id):
        return self.notifications_repository.remove_all_notifications_by_user_id(user_id)

    def update_notification(self, notification):
        return self.notifications_repository.update_notification(notification)

    def add_note(self, note):
        return self.notes_repository.add_note(note)

    def get_note_by_id(self, note_id):
        return self.notes_repository.get_note_by_id(note_id)

    def get_all_notes_by_user_id(self, user_id):
        return self.notes_repository.get_all_notes_by_user_id(user_id)

    def remove_note(self, note_id):
        return self.notes_repository.remove_note(note_id)

    def update_note(self, note):
        return self.notes_repository.update_note(note)

    def get_last_note(self):
        return self.notes_repository.get_last_note()