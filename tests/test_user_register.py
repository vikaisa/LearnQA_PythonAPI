import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

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

    @pytest.mark.parametrize("data", data_for_unsuccessful_register)
    def test_create_user_wo_one_of_the_fields(self, data):
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content.decode("utf-8"))

    def test_create_user_with_very_short_username(self):
        data = {"password": "123", "email": "vinkotov@example.com", "username": "l", "firstName": "learnqa", "lastName": "learnqa"}
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_very_long_username(self):
        data = {"password": "123", "email": "vinkotov@example.com",
                "username": "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "firstName": "learnqa", "lastName": "learnqa"}
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"
