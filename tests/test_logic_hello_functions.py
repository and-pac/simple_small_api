import unittest
import mock
from datetime import date
from freezegun import freeze_time

import sys,os
sys.path.insert(0, os.path.abspath('./src'))

from logic.hello_functions import *

def static_get_dob(username):
    static_db = {
        "usernameone"  : [(date(1980,1,1),)],
        "usernametwo"  : [(date(1980,2,29),)],
        "usernamethree": [(date(1980,10,22),)]

    }
    try:
        return static_db[username]
    except KeyError:
        return [()]

def static_upsert_dob(user,dob):
        return 1

def static_upsert_dob_error(user,dob):
        raise psycopg2.OperationalError('Mock db error')


class TestLogic(unittest.TestCase):
    def test_get_user_and_validate_path(self):
        assert get_user_and_validate_path('/') == -1
        assert get_user_and_validate_path('//') == -1
        assert get_user_and_validate_path('/nothello/alpha') == -1
        assert get_user_and_validate_path('/hello/alpha1') == -1
        assert get_user_and_validate_path('/hello/1alpha') == -1
        assert get_user_and_validate_path('/hello/alpha/1') == -1
        assert get_user_and_validate_path('/hello/$alpha') == -1
        assert get_user_and_validate_path('/hello/\alpha') == -1
        assert get_user_and_validate_path('/hello/alpha?blabla') == "alpha"
        assert get_user_and_validate_path('/hello/alpha') == "alpha"
        assert get_user_and_validate_path('/health') == "200"

    @mock.patch('logic.hello_functions.get_dob', side_effect=static_get_dob)
    @freeze_time('2021-10-22')
    def test_get_birthday_response(self, get_dob_function):
        assert get_birthday_response("usernameone") == (200,{"message": "Hello, usernameone! Your birthday is in 71 day(s)"})
        assert get_birthday_response("usernametwo") == (200,{"message": "Hello, usernametwo! Your birthday is in 860 day(s)"})
        assert get_birthday_response("usernamethree") == (200,{"message": "Hello, usernamethree! Happy Birthday!"})
        assert get_birthday_response("usernamefour") == (404,{})

    @mock.patch('logic.hello_functions.upsert_dob', side_effect=static_upsert_dob)
    @freeze_time('2021-10-22')
    def test_upsert_and_validate_json(self, upsert_dob_function):
        assert upsert_and_validate_json("usernameone",'{ "dateOfBirth": "1980-02-29" }') == (204)
        assert upsert_and_validate_json("usernameone",'{ "dateOfBirth": "2021-10-22" }') == (400)
        assert upsert_and_validate_json("usernameone",'{ "dateOfBirth": "2021-10-23" }') == (400)
        assert upsert_and_validate_json("usernameone",'{ "dateOfBirth": "2001-02-29" }') == (400)
        assert upsert_and_validate_json("usernameone",'not json') == (411)
        assert upsert_and_validate_json("usernameone",'') == (411)

        upsert_dob_function.side_effect=static_upsert_dob_error  
        assert upsert_and_validate_json("usernameone",'{ "dateOfBirth": "1980-02-29" }') == (503)

