import pytest
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from allure import severity, severity_level


@allure.link("https://playground.learnqa.ru/api/map", name="API Description")
@allure.epic("User cases")
@allure.feature("User's registration")
@allure.story("As a user I want to register an account")
@severity(severity_level.BLOCKER)
class TestUserRegister(BaseCase):
    @allure.title("Successful registration")
    @allure.description("This test checks an opportunity to register a user's account successfully")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Unsuccessful registration")
    @allure.description("This test checks an opportunity to register a user's account with an existing email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.title("Unsuccessful registration")
    @allure.description("This test checks an opportunity to register a user's account with an incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    data_for_unsuccessful_register = [
        ({"password": "123", "username": "learnqa", "firstName": "learnqa", "lastName": "learnqa"}),
        ({"email": "vinkotov@example.com", "username": "learnqa", "firstName": "learnqa", "lastName": "learnqa"}),
        ({"email": "vinkotov@example.com", "password": "123", "firstName": "learnqa", "lastName": "learnqa"}),
        ({"email": "vinkotov@example.com", "username": "learnqa", "password": "123", "lastName": "learnqa"}),
        ({"email": "vinkotov@example.com", "username": "learnqa", "password": "123", "firstName": "learnqa"})]

    @allure.title("Unsuccessful registration")
    @allure.description("This test checks an opportunity to register a user's account without one of the required fields")
    @pytest.mark.parametrize("data", data_for_unsuccessful_register)
    def test_create_user_wo_one_of_the_fields(self, data):
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content.decode("utf-8"))

    @allure.title("Unsuccessful registration")
    @allure.description("This test checks an opportunity to register a user's account with an very short username")
    def test_create_user_with_very_short_username(self):
        data = {"password": "123", "email": "vinkotov@example.com", "username": "l", "firstName": "learnqa", "lastName": "learnqa"}
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.title("Unsuccessful registration")
    @allure.description("This test checks an opportunity to register a user's account with an very long username")
    def test_create_user_with_very_long_username(self):
        data = {"password": "123", "email": "vinkotov@example.com",
                "username": "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "firstName": "learnqa", "lastName": "learnqa"}
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"
