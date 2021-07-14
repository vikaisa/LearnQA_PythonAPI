from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    # def test_edit_just_created_user(self):
    #     # REGISTER
    #     register_data = self.prepare_registration_data()
    #     response1 = MyRequests.post("/user/", data=register_data)
    #
    #     Assertions.assert_code_status(response1, 200)
    #     Assertions.assert_json_has_key(response1, "id")
    #
    #     email = register_data["email"]
    #     first_name = register_data["firstName"]
    #     password = register_data["password"]
    #     user_id = self.get_json_value(response1, "id")
    #
    #     # LOGIN
    #     login_data = {"email": email, "password": password}
    #     response2 = MyRequests.post("/user/login", data=login_data)
    #
    #     auth_sid = self.get_cookie(response2, "auth_sid")
    #     token = self.get_header(response2, "x-csrf-token")
    #
    #     # EDIT
    #     new_name = "Changed Name"
    #     response3 = MyRequests.put(f"/user/{user_id}",
    #                                headers={"x-csrf-token": token},
    #                                cookies={"auth_sid": auth_sid},
    #                                data={"firstName": new_name})
    #
    #     Assertions.assert_code_status(response3, 200)
    #
    #     # GET
    #     response4 = MyRequests.get(f"/user/{user_id}",
    #                                headers={"x-csrf-token": token},
    #                                cookies={"auth_sid": auth_sid})
    #
    #     Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong user name after editing")

    def test_edit_user_being_unauthorized(self):
        # EDIT
        new_username = "new_name"
        response1 = MyRequests.put("/user/2", data={"username": new_username})
        Assertions.assert_code_status(response1, 400)
        assert response1.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response1.content}"

        # CHECK CHANGES
        response2 = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response2, "username")
        response_as_dict = response2.json()
        assert response_as_dict["username"] == "Vitaliy", f"Username field value was changed to {response_as_dict['username']}"

    def test_edit_user_being_authorized_as_another_one(self):
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

        # EDIT
        new_username = "new_name"
        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}, data={"username": new_username})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Please, do not edit test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response3.content}"

        # CHECK CHANGES
        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_json_has_key(response4, "username")
        response_as_dict = response4.json()
        assert response_as_dict["username"] == "learnqa", f"Username field value was changed to {response_as_dict['username']}"

    def test_edit_user_email_incorrectly(self):
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

        # EDIT
        new_email = "new_emailgmail.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response3.content}"

        # CHECK CHANGES
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_has_key(response4, "email")
        response_as_dict = response4.json()
        assert response_as_dict["email"] == email, f"Email field value was changed to {response_as_dict['email']}"

    def test_edit_user_first_name_incorrectly(self):
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

        # EDIT
        new_first_name = "n"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_first_name})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', \
            f"Unexpected response content {response3.content}"

        # CHECK CHANGES
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_has_key(response4, "firstName")
        response_as_dict = response4.json()
        assert response_as_dict["firstName"] == "learnqa", f"FirstName field value was changed to {response_as_dict['firstName']}"