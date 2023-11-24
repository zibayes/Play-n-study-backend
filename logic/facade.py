from sqlalchemy import func

from data.types import SubRel, CourseRel, CourseUnit, Course, UserProgress, Review, ChatMessage
from logic.data_facade import DataFacade
from logic.auth.auth import Auth
from logic.test import get_test_from_form, get_test_result

# todo: сделать единые названия для функций фасада,
#  если связано с тестами test_get_by_id, пользователями user_get_for_profile, user_get_for_courses и тд


class LogicFacade:
    def __init__(self, session):
        self.data = DataFacade(session)
        self.auth = Auth(session)

    def get_user_for_profile(self, user_id, current_user_id):
        return self.data.get_user_for_profile(user_id, current_user_id)

    def get_user_for_courses(self, user_id):
        return self.data.get_user_for_courses(user_id)

    def get_user_by_id(self, user_id):
        return self.data.get_user_by_id(user_id)

    def user_auth(self, email_or_username, password):
        return self.auth.user_auth(email_or_username, password)

    def user_register(self, form):
        return self.auth.user_register(form)

    def get_user_for_subscriptions(self, user_id):
        return self.data.get_user_for_subscriptions(user_id)

    def get_users_by_query(self, query):
        return self.data.get_users_by_query(query)

    def user_avatar_upload(self, file, current_user):
        # todo: вынести в отдельный файл
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                user = self.data.get_user_by_id(current_user.get_id())
                user.avatar = img
                res = self.data.upload_avatar(user)
                if not res:
                    return tuple(["Ошибка обновления аватара", "error"])
                return tuple(["Аватар обновлен", "success"])
            except FileNotFoundError as e:
                return tuple (["Ошибка чтения файла", "error"])
        else:
            return tuple(["Ошибка обновление аватара", "error"])

    def get_user_avatar(self, app, user_id):
        return self.data.get_user_avatar(app, user_id)

    def save_test(self, form, files, course_id, unit_id):
        test = get_test_from_form(form=form, files=files, unit_id=unit_id, course_id=course_id)
        if self.data.add_test(test):
            test = self.data.get_last_test_by_course(course_id)
            course = self.data.course_get_by_id(course_id)
            for unit in course.content['body']:
                if int(unit['unit_id']) == unit_id:
                    unit['tests'].append(CourseUnit(unit_type='test', test_id=test.test_id))
            self.data.update_course(course)
            return tuple(['Тест успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении теста', 'error'])

    def upload_test_avatar(self, avatar_file, current_user, test_id):
        if avatar_file and current_user.verify_ext(avatar_file.filename):
            try:
                avatar = avatar_file.read()
                test = self.data.get_test_by_id(test_id)
                test.avatar = avatar
                test.content = test.content.toJSON()
                if not self.data.update_test(test):
                    return tuple(["Ошибка обновления аватара", "error"])
                return tuple(["Аватар обновлен", "success"])
            except FileNotFoundError as e:
                return tuple(["Ошибка чтения файла", "error"])
        else:
            return tuple(["Ошибка обновление аватара", "error"])


    def add_course(self, course_name, course_desc, course_cat, avatar_file, current_user, user_id):
        '''
        if avatar_file and current_user.verify_ext(avatar_file.filename):
            try:
                avatar = avatar_file.read()
            except FileNotFoundError as e:
                return tuple(["Ошибка чтения файла", "error"])
        else:
            return tuple(["Ошибка обновление аватара", "error"])
        '''
        course = Course(course_id=None, name=course_name, description=course_desc, category=course_cat, avatar=None, content={'body': [], 'unit_counter': 0})
        if self.data.add_course(course):
            course = self.data.get_last_course()
            self.course_join(course.course_id, user_id)
            return tuple(['Курс успешно сохранён', 'success', course.course_id])
        else:
            return tuple(['Ошибка при сохранении курса', 'error'])

    def upload_course_avatar(self, avatar_file, current_user):
        if avatar_file and current_user.verify_ext(avatar_file.filename):
            try:
                return avatar_file.read()
            except FileNotFoundError as e:
                return tuple(["Ошибка чтения файла", "error"])
        else:
            return tuple(["Ошибка обновления аватара", "error"])

    def update_course_add_unit(self, course_id, unit_name):
        course = self.data.course_get_by_id(course_id)
        course.content['unit_counter'] += 1
        course.content['body'].append({'name': unit_name, 'unit_id': course.content['unit_counter'], 'tests': []})
        if self.data.update_course(course):
            return tuple(['Раздел успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении раздела курса', 'error'])

    def update_course(self, course):
        if self.data.update_course(course):
            return tuple(['Курс успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении курса', 'error'])

    def remove_course(self, course_id):
        if self.data.remove_course(course_id):
            return tuple(['Курс успешно удалён', 'success'])
        else:
            return tuple(['Ошибка при удалении курса', 'error'])

    def remove_test(self, test_id):
        return self.data.remove_test(test_id)

    def get_test_by_id(self, test_id):
        return self.data.get_test_by_id(test_id)

    def get_all_tests(self):
        return self.data.get_all_tests()

    def edit_test(self, form, files, test_id, course_id, unit_id):
        test = get_test_from_form(form=form, files=files, test_id=test_id, course_id=course_id, unit_id=unit_id)
        test.avatar = self.data.get_test_by_id(test_id).avatar

        if self.data.update_test(test):
            return tuple(['Тест успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении теста', 'error'])

    def get_test_result(self, test, form):
        return get_test_result(test, form)

    def add_progress(self, course_id, user_id, task_id, task_type, progress):
        user_progress = UserProgress(up_id=None, course_id=course_id, user_id=user_id, task_id=task_id, task_type=task_type, progress=progress)
        if self.data.add_progress(user_progress):
            return tuple(['Прогресс успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении прогресса', 'error'])

    def remove_progress(self, up_id):
        if self.data.remove_progress(up_id):
            return tuple(['Прогресс успешно удалён', 'success'])
        else:
            return tuple(['Ошибка при удалении прогресса', 'error'])

    def update_progress(self, progress):
        if self.data.update_progress(progress):
            return tuple(['Прогресс успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении прогресса', 'error'])

    def get_last_progress_by_task(self, user_id, course_id, task_id, task_type):
        return self.data.get_last_progress_by_task(user_id, course_id, task_id, task_type)

    def add_review(self, user_id, course_id, rate):
        review = Review(None, user_id, course_id, rate, None)
        return self.data.add_review(review)

    def get_reviews_by_course_id(self, course_id):
        return self.data.get_reviews_by_course_id(course_id)

    def update_review(self, user_id, course_id, rate, text):
        review = Review(None, user_id, course_id, rate, text)
        return self.data.update_review(review)

    def change_user_data(self, form, current_user_id):
        # todo: вынести в отдельный файл
        user = self.data.get_user_by_id(current_user_id)
        username = self.data.get_user_by_username(form.get('username'))
        if username is not None and username.user_id != user.user_id:
            return tuple(["Такое имя уже занято", 'error'])
        else:
            user.username = form.get('username')

        email = self.data.get_user_by_email(form.get('email'))
        if email is not None and email.user_id != user.user_id:
            return tuple(["Такой email уже занят"])
        else:
            user.email = form.get('email')

        user.city = form.get('city')
        if self.data.update_user(user):
            return tuple(["Успешно обновлено"])
        else:
            return tuple(["Что-то пошло не так"])

    def add_sub_relation(self, user_id, cur_user_id):
        subrel = SubRel(
            sub_rel_id=None,
            user_id=user_id,
            sub_id=cur_user_id
        )
        if self.data.add_sub_rel(subrel):
            return True
        return False

    def remove_sub_relation(self, user_id, cur_user_id):
        need_row = self.data.sub_rel_repository.\
            get_one_by_user_and_sub_ids(user_id, cur_user_id)
        if self.data.sub_rel_repository.remove_sub_rel_by_id(need_row.sub_rel_id):
            return True
        else:
            return False

    def forum_get_avatar(self, app, forum_id):
        return self.data.forum_get_avatar(app, forum_id)

    def link_get_avatar(self, app, link_id):
        return self.data.link_get_avatar(app, link_id)

    def article_get_avatar(self, app, article_id):
        return self.data.article_get_avatar(app, article_id)

    def test_get_avatar(self, app, test_id):
        return self.data.test_get_avatar(app, test_id)

    def course_get_avatar(self, app, course_id):
        return self.data.course_get_avatar(app, course_id)

    def courses_get_by_query(self, query):
        return self.data.course_get_courses_by_query(query)

    def course_get_by_id(self, course_id):
        return self.data.course_get_by_id(course_id)

    def course_join(self, course_id, user_id):
        course_rel = CourseRel(
            cour_rel_id=None,
            user_id=user_id,
            course_id=course_id
        )
        if self.data.rel_add_course_rel(course_rel):
            return True
        return False

    def course_leave(self, course_id, user_id):
        need_row = self.data.course_rel_repository. \
            get_one_by_user_and_course_ids(user_id, course_id)
        if self.data.course_rel_repository.rel_remove_course_rel(need_row.cour_rel_id):
            return True
        else:
            return False

    def get_course_rels_all(self, course_id):
        return self.data.get_course_rels_all(course_id)

    def rel_remove_course_rel(self, rel_id):
        return self.data.rel_remove_course_rel(rel_id)

    def article_get_by_id(self, article_id):
        return self.data.article_get_by_id(article_id)

    def article_get_all_by_course_id(self, course_id):
        return self.data.article_get_all_by_course_id(course_id)

    def article_add_article(self, article, course_id, unit_id, task_type):
        if self.data.article_add_article(article):
            article = self.data.get_last_article_by_course(course_id)
            course = self.data.course_get_by_id(course_id)
            for unit in course.content['body']:
                if int(unit['unit_id']) == unit_id:
                    unit['tests'].append(CourseUnit(unit_type=task_type, test_id=article.article_id))
            self.data.update_course(course)
            return tuple(['Статья успешно сохранена', 'success'])
        else:
            return tuple(['Ошибка при сохранении статьи', 'error'])

    def update_article(self, article, course_id, unit_id, task_type):
        course = self.data.course_get_by_id(course_id)
        for unit in course.content['body']:
            if int(unit['unit_id']) == unit_id:
                for test in unit['tests']:
                    if test.test_id == article.article_id and test.unit_type == task_type:
                        unit['tests'][unit['tests'].index(test)] = CourseUnit(unit_type=task_type,
                                                                              test_id=article.article_id)
        self.data.update_course(course)
        return self.data.update_article(article)

    def remove_article(self, article_id):
        return self.data.remove_article(article_id)

    def link_add_link(self, link, course_id, unit_id):
        if self.data.link_add_link(link):
            link = self.data.get_last_link_by_course(course_id)
            course = self.data.course_get_by_id(course_id)
            for unit in course.content['body']:
                if int(unit['unit_id']) == unit_id:
                    unit['tests'].append(CourseUnit(unit_type='link', test_id=link.link_id))
            self.data.update_course(course)
            return tuple(['Ссылка успешно сохранена', 'success'])
        else:
            return tuple(['Ошибка при сохранении ссылки', 'error'])

    def link_get_by_id(self, link_id):
        return self.data.link_get_by_id(link_id)

    def link_get_all_by_course_id(self, course_id):
        return self.data.link_get_all_by_course_id(course_id)

    def get_last_link_by_course(self, link_id):
        return self.data.get_last_link_by_course(link_id)

    def update_link(self, link):
        return self.data.update_link(link)

    def remove_link(self, link_id):
        return self.data.remove_link(link_id)

    def forum_get_by_id(self, forum_id):
        return self.data.get_forum_by_id(forum_id)

    def forum_get_all_by_course_id(self, course_id):
        return self.data.forum_get_all_by_course_id(course_id)

    def forum_add_forum(self, forum):
        if self.data.forum_add_forum(forum):
            forum = self.data.get_last_forum_by_course(forum.course_id)
            course = self.data.course_get_by_id(forum.course_id)
            for unit in course.content['body']:
                if int(unit['unit_id']) == forum.unit_id:
                    unit['tests'].append(CourseUnit(unit_type='forum', test_id=forum.forum_id))
            self.data.update_course(course)
            return tuple(['Форум успешно сохранен', 'success'])
        else:
            return tuple(['Ошибка при сохранении форума', 'error'])

    def get_last_forum_by_course(self, forum_id):
        return self.data.get_last_forum_by_course(forum_id)

    def update_forum(self, forum):
        return self.data.update_forum(forum)

    def remove_forum(self, forum_id):
        return self.data.remove_forum(forum_id)

    def forum_topic_get_by_id(self, ft_id):
        return self.data.forum_topic_get_by_id(ft_id)

    def topic_get_all_by_forum_id(self, forum_id):
        return self.data.topic_get_all_by_forum_id(forum_id)

    def forum_topic_add_forum_topic(self, forum_topic):
        return self.data.forum_topic_add_forum_topic(forum_topic)

    def get_last_topic_by_forum(self, forum_id):
        return self.data.get_last_topic_by_forum(forum_id)

    def update_forum_topic(self, forum_topic):
        return self.data.update_forum_topic(forum_topic)

    def remove_forum_topic(self, ft_id):
        return self.data.remove_forum_topic(ft_id)

    def get_topics_by_query(self, query, forum_id):
        return self.data.get_topics_by_query(query, forum_id)

    def topic_message_get_by_id(self, tm_id):
        return self.data.topic_message_get_by_id(tm_id)

    def messages_get_all_by_topic_id(self, ft_id):
        return self.data.messages_get_all_by_topic_id(ft_id)

    def add_topic_message(self, topic_message):
        return self.data.add_topic_message(topic_message)

    def get_last_message_by_topic(self, ft_id):
        return self.data.get_last_message_by_topic(ft_id)

    def update_topic_message(self, topic_message):
        return self.data.update_topic_message(topic_message)

    def remove_topic_message(self, tm_id):
        return self.data.remove_topic_message(tm_id)

    def course_get_for_preview(self, course_id, user_id):
        course = self.course_get_by_id(course_id)
        rel = self.data.course_rel_repository.get_one_by_user_and_course_ids(user_id, course_id)
        if rel is None:
            course.can_subscribe = True
        else:
            course.can_subscribe = False
        return course

    def user_progress_get_by_user_course_ids(self, user_id, course_id):
        return self.data.user_get_progress_by_course_user_ids(user_id, course_id)

    def get_progress_by_id(self, progress_id):
        return self.data.get_progress_by_id(progress_id)

    def get_progress_by_user_course_ids_all(self, user_id, course_id):
        return self.data.get_progress_by_user_course_ids_all(user_id, course_id)

    def get_progress_by_course_id_all(self, course_id):
        return self.data.get_progress_by_course_id_all(course_id)

    def get_course(self, course_id, user_id):
        course = self.data.course_json_get_by_id(course_id)
        rel = self.data.course_rel_repository.get_one_by_user_and_course_ids(user_id, course_id)
        if rel is None:
            return
        return course

    def get_course_without_rel(self, course_id):
        return self.data.course_json_get_by_id(course_id)

    def __role_get_user_role_by_user_id(self, user_id):
        return self.data.role_get_user_roles_by_user_id(user_id)

    def role_get_user_role_by_user_id(self, user_id):
        return self.data.role_get_user_roles_by_user_id(user_id)

    def add_user_role_admin(self, user_id):
        return self.data.add_user_role_admin(user_id)

    def remove_user_role_admin(self, user_id):
        return self.data.remove_user_role_admin(user_id)

    def is_user_admin(self, user_id):
        roles = self.__role_get_user_role_by_user_id(user_id)
        if roles and 'admin' in roles:
            return True
        return False

    def is_user_curator_of_course(self, user_id, course_id):
        return self.data.is_user_curator_of_course(user_id, course_id)

    def get_curators_by_course_id(self, course_id):
        return self.data.get_curators_by_course_id(course_id)

    def curator_add(self, user_id, course_id):
        return self.data.curator_add(user_id, course_id)

    def curator_remove(self, user_id, course_id):
        return self.data.curator_remove(user_id, course_id)

    def chats_start_dialog(self, current_user_id, user_id):
        if not self.data.chat_exists(current_user_id, user_id):
            return self.data.chats_start_dialog(current_user_id, user_id)

    def chats_get_user_chats_preview(self, user_id):
        return self.data.chat_get_user_chats_preview(user_id)

    def chats_get_dialog(self, user_id, chat_id):
        return self.data.chat_get_dialog(user_id, chat_id)

    def remove_message(self, msg_id):
        return self.data.remove_message(msg_id)

    def update_chat_message(self, message, msg_id):
        return self.data.update_chat_message(message['msg_text'], msg_id)

    def get_last_chat_message_by_id(self, chat_id):
        return self.data.get_last_chat_message_by_id(chat_id)

    def get_chat_by_users(self, msg_from, msg_to):
        return self.data.chat_repository.get_chat_id(msg_from, msg_to)

    def chats_send_message(self, req_json, user_id):
        # if chat exists -> send message, else create_chat -> send_message
        msg_text = req_json['msg_text']
        msg_from = user_id
        msg_to = int(req_json['msg_to'])

        if self.__chat_exists(msg_from, msg_to):
            chat_id = self.data.chat_repository.get_chat_id(msg_from, msg_to)
            if chat_id is not None:
                return self.__chat_send_message(chat_id, msg_text, msg_from, msg_to)
            return False

        chat_id = None
        created = self.__chat_create(msg_from, msg_to)
        if created:
            chat_id = self.data.chat_repository.get_chat_id(msg_from, msg_to)
        else:
            # create error
            return False
        if chat_id is not None:
            return self.__chat_send_message(chat_id, msg_text, msg_from, msg_to)
        return False

    def __chat_send_message(self, chat_id, msg_text, msg_from, msg_to):
        message = ChatMessage(None, chat_id, msg_text, None, msg_from, msg_to, False)

        # sending message
        response = self.data.chat_messages_repository.send_message(message)

        # change checked status
        response2 = self.data.chat_change_check_status(chat_id, msg_to)

        return response, response2

    def __chat_exists(self, user_from, user_to) -> bool:
        return self.data.chat_exists(user_from, user_to)

    def __chat_create(self, msg_from, msg_to):
        return self.data.chat_repository.create(msg_from, msg_to)

    def remove_chat(self, chat_id):
        return self.data.remove_chat(chat_id)