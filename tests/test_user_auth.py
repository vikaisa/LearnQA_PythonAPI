import pytest
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

from allure import severity, severity_level


@allure.link("https://playground.learnqa.ru/api/map", name="API Description")
@allure.epic("User cases")
@allure.feature("Authorization")
@allure.story("As a user I want to authorize with an email and a password")
@severity(severity_level.BLOCKER)
class TestUserAuth(BaseCase):
    excluded_params = [("no_cookie"), ("no_token")]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.title("Successful authorization")
    @allure.description("This test successfully authorizes a user by an email and a password")
    def test_auth_user(self):
        response2 = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "User id from auth method does not equal user id from check method")

    @allure.title("Unsuccessful authorization")
    @allure.description("This test checks an authorization status w/o sending an auth cookie or a token")
    @pytest.mark.parametrize("condition", excluded_params)
    def test_negative_auth_check_self(self, condition):
        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth",
                                       headers={"x-csrf-token": self.token})
        else:
            response2 = MyRequests.get("/user/auth", cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", 0,
                                             f"User is authorized despite the condition {condition}")
