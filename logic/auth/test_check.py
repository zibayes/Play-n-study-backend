"""Тесты для модуля check"""

import unittest
from data.types import *
from logic.auth.check import *


TEST_DATA_GET_REGISTER_FROM_FIELDS = [
    ({'email': 'email', 'username': 'username', 'password': 'password', 'password2': 'password2'}, ('email', 'username', 'password', 'password2')),
    ({'email': 'test', 'username': 'test1', 'password': 'test2', 'password2': 'test3'}, ('test', 'test1', 'test2', 'test3')),
    ({'email': 'ziba_yes', 'username': 'ziba_yes', 'password': 'ziba_yes', 'password2': 'ziba_yes'}, ('ziba_yes', 'ziba_yes', 'ziba_yes', 'ziba_yes')),
    ({'email': 'sanchello13pv@mail.ru', 'username': 'ziba_yes', 'password': '1234', 'password2': '1234'}, ('sanchello13pv@mail.ru', 'ziba_yes', '1234', '1234')),
]

TEST_DATA_AM_I_SUBSCRIBER_OF = [
    ([User(user_id=0), User(user_id=1), User(user_id=2)], User(user_id=0), True),
    ([User(user_id=0), User(user_id=1), User(user_id=2)], User(user_id=4), False),
    ([User(user_id=5), User(user_id=1), User(user_id=2)], User(user_id=1), True),
    ([User(user_id=5), User(user_id=1), User(user_id=2), User(user_id=3), User(user_id=4)], User(user_id=0), False),
    ([User(user_id=5), User(user_id=1), User(user_id=2), User(user_id=3), User(user_id=4)], User(user_id=3), True),
]


class TestCheck(unittest.TestCase):
    """Тест-кейс модуля check"""
    def test_get_register_form_fields(self):
        """Тест функции get_register_form_fields"""
        for fields, expected in TEST_DATA_GET_REGISTER_FROM_FIELDS:
            with self.subTest():
                self.assertEqual(get_register_form_fields(fields), expected)

    def test_am_i_subscriber_of(self):
        """Тест функции am_i_subscriber_of"""
        for sub_to, user, expected in TEST_DATA_AM_I_SUBSCRIBER_OF:
            with self.subTest():
                self.assertEqual(am_i_subscriber_of(sub_to, user), expected)
