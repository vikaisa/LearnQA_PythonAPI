import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from allure import severity, severity_level


@allure.link("https://playground.learnqa.ru/api/map", name="API Description")
@allure.epic("User cases")
@allure.feature("Getting user's info")
@allure.story("As a user I want to get my profile's info")
@severity(severity_level.CRITICAL)
class TestUserGet(BaseCase):
    @allure.title("Getting profile's info as unauthorized user")
    @allure.description("This test checks an opportunity to get certain user's profile info being unauthorized")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    @allure.title("Getting profile's info being logged in as this user")
    @allure.description("This test checks an opportunity to get all user's profile info being logged in as this user")
    def test_get_user_details_auth_as_same_user(self):
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=payload)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Getting profile's info being logged in as another user")
    @allure.description("This test checks an opportunity to get a particular kind of user's profile info being logged in as another user")
    def test_get_user_details_auth_as_another_user(self):
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = MyRequests.post("/user/login", data=payload)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        response2 = MyRequests.get("/user/1",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_no_key(response2, "email")
        Assertions.assert_json_has_no_key(response2, "firstName")
        Assertions.assert_json_has_no_key(response2, "lastName")
