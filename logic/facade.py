from data.types import SubRel, CourseRel, CourseUnit
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

    def save_test(self, form, course_id, unit_id):
        test = get_test_from_form(form)
        test.course_id = course_id
        if self.data.add_test(test):
            test = self.data.get_last_test_by_course(course_id)
            course = self.data.course_get_by_id(course_id)
            for unit in course.content:
                if int(unit['unit_id']) == unit_id:
                    unit['tests'].append(CourseUnit(unit_type='test', test_id=test.test_id))
            self.data.update_course(course)
            return tuple(['Тест успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении теста', 'error'])

    def get_test_by_id(self, test_id):
        return self.data.get_test_by_id(test_id)

    def get_all_tests(self):
        return self.data.get_all_tests()

    def edit_test(self, form):
        test = get_test_from_form(form)

        # change if you need
        test.course_id = 1

        if self.data.update_test(test):
            return tuple(['Тест успешно сохранён', 'success'])
        else:
            return tuple(['Ошибка при сохранении теста', 'error'])

    def get_test_result(self, test, form):
        return get_test_result(test, form)

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

    def get_course(self, course_id, user_id):
        course = self.data.course_json_get_by_id(course_id)
        rel = self.data.course_rel_repository.get_one_by_user_and_course_ids(user_id, course_id)
        if rel is None:
            return
        return course