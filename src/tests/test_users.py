import unittest
from tests.helpers import Helpers
from main import create_app, db


class TestUsers(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        result_seed = runner.invoke(args=["db-custom", "seed"])
        if result_seed.exit_code != 0:
            raise ValueError(result_seed.stdout)

        cls.headers = {}
        for i in range(1, 6):
            cls.login = cls.client.post(
                "users/login",
                json={
                    "email": f"test{i}@test.com",
                    "password": "123456"
                }
            )
            cls.token = cls.login.get_json()["token"]
            cls.header = {"Authorization": f"Bearer {cls.token}"}
            cls.headers[f"test{i}"] = cls.header
        cls.headers["fakeuser"] = {"Authorization": "Bearer invalid_token"}

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    # def post_request(self, endpoint, header=None, body=None):
    #     response = self.client.post(endpoint, headers=header, json=body)
    #     data = response.get_json()
    #     return (response, data)

    # def get_request(self, endpoint, header=None):
    #     response = self.client.get(endpoint, headers=header)
    #     data = response.get_json()
    #     return (response, data)

    # def patch_request(self, endpoint, header, body):
    #     response = self.client.patch(endpoint, headers=header, json=body)
    #     data = response.get_json()
    #     return (response, data)

    # def delete_request(self, endpoint, header=None):
    #     response = self.client.delete(endpoint, headers=header)
    #     data = response.get_json()
    #     return (response, data)

    def test_users_register(self):
        endpoint = "/users/register"
        body = {
                "email": "user1@testing.com",
                "password": "abcdef",
                "subscription_status": "1"}
        response, data = Helpers.post_request(endpoint, body=body)
        response2, data2 = Helpers.post_request(endpoint, body=body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["user_id"], 6)
        self.assertEqual(data["email"], "user1@testing.com")
        self.assertEqual(data["subscription_status"], True)
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)

    def test_users_login(self):
        endpoint = "/users/login"
        body = {
            "email": "test1@test.com",
            "password": "123456"
        }
        body2 = {
            "email": "test6@test.com",
            "password": "abcdef"
        }
        response, data = Helpers.post_request(endpoint, body=body)
        response2, data2 = Helpers.post_request(endpoint, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)
        self.assertIsInstance(data["token"], str)
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)

    def test_get_user(self):
        endpoint = "/users/"
        response, data = Helpers.get_request(endpoint, self.headers["test1"])
        response2, data2 = Helpers.get_request(endpoint)
        response3, data3 = Helpers.get_request(
            endpoint, self.headers["fakeuser"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["user_id"], 1)
        self.assertEqual(len(data), 3)
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(response3.status_code, 422)

    def test_update_user(self):
        endpoint = "/users/"
        body = {
                "email": "abc@test.com",
                "subscription_status": "false"
            }
        body2 = {
                "email": "123@456.com",
                "subscription_status": "true"
            }
        response, data = Helpers.patch_request(
            endpoint, self.headers["test1"], body)
        response2, data2 = Helpers.patch_request(
            endpoint, self.headers["test2"], body2)
        user1 = Helpers.get_request(endpoint, self.headers["test1"])
        user2 = Helpers.get_request(endpoint, self.headers["test2"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(user1[1]["email"], "abc@test.com")
        self.assertEqual(user2[1]["subscription_status"], True)

    def test_delete_user(self):
        endpoint = "/users/"
        header = self.headers["test5"]

        before_delete = Helpers.get_request(endpoint, header=header)
        delete = Helpers.delete_request(endpoint, header=header)
        after_delete = Helpers.get_request(endpoint, header=header)
        delete2 = Helpers.delete_request(endpoint, header=header)

        self.assertEqual(before_delete[0].status_code, 200)
        self.assertEqual(before_delete[1]["user_id"], 5)
        self.assertEqual(delete[0].status_code, 200)
        self.assertEqual(delete[1]["user_id"], 5)
        self.assertEqual(after_delete[0].status_code, 404)
        self.assertIsNone(after_delete[1])
        self.assertEqual(delete2[0].status_code, 404)
