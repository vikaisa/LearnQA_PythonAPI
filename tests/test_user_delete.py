import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from allure import severity, severity_level


@allure.link("https://playground.learnqa.ru/api/map", name="API Description")
@allure.epic("User cases")
@allure.feature("Deletion")
@allure.story("As a user I want to delete my profile")
@severity(severity_level.CRITICAL)
class TestUserDelete(BaseCase):
    @allure.title("Unsuccessful deletion")
    @allure.description("This test checks an inability to delete users protected from deletion")
    def test_delete_user_that_cannot_be_deleted(self):
        # LOGIN
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = MyRequests.post("/user/login", data=payload)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    @allure.title("Successful deletion")
    @allure.description("This test checks an opportunity to delete a user's profile being logged in as this user")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {"email": email, "password": password}
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 200)

        # CHECK DELETION
        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response4.content}"

    @allure.title("Unsuccessful deletion")
    @allure.description("This test checks an opportunity to delete a user's profile being logged in as another user")
    def test_delete_user_being_authorized_as_another_one(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # LOGIN
        payload = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response2 = MyRequests.post("/user/login", data=payload)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response3.content}"

        # CHECK CHANGES
        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_json_has_key(response4, "username")
        Assertions.assert_code_status(response4, 200)
