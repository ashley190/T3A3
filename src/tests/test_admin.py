import unittest
from tests.helpers import Helpers
from main import create_app, db
import random


class TestAdmin(unittest.TestCase):
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
        for i in range(1, 3):
            cls.login = cls.client.post(
                "admin/login",
                json={
                    "username": f"Admin{i}",
                    "password": "654321"
                }
            )
            cls.token = cls.login.get_json()["token"]
            cls.header = {"Authorization": f"Bearer {cls.token}"}
            cls.headers[f"Admin{i}"] = cls.header
        cls.headers["fakeadmin"] = {"Authorization": "Bearer invalid_token"}

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_admin_login(self):
        endpoint = "admin/login"
        body1 = {
            "username": "Admin1",
            "password": "654321"
        }
        body2 = {
            "username": "Admin3",
            "password": "fedcba"
        }

        response, data = Helpers.post_request(endpoint, body=body1)
        response2, data2 = Helpers.post_request(endpoint, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)
        self.assertIsInstance(data["token"], str)
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)

    def test_get_users(self):
        endpoint = "/admin/users"
        header = self.headers["Admin1"]
        header2 = self.headers["fakeadmin"]

        response, data = Helpers.get_request(endpoint, header)
        response2, data2 = Helpers.get_request(endpoint)
        response3, data3 = Helpers.get_request(endpoint, header2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 5)
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(response3.status_code, 422)

    def test_get_groups(self):
        endpoint = "/admin/groups"
        header = self.headers["Admin2"]
        header2 = self.headers["fakeadmin"]

        response, data = Helpers.get_request(endpoint, header)
        response2, data2 = Helpers.get_request(endpoint, header2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 10)
        self.assertEqual(response2.status_code, 422)

    def test_get_content(self):
        endpoint = "/admin/content"
        header = self.headers["Admin1"]
        header2 = self.headers["fakeadmin"]

        response, data = Helpers.get_request(endpoint, header)
        response2, data2 = Helpers.get_request(endpoint, header2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 30)
        self.assertEqual(response2.status_code, 422)

    def test_get_group_content(self):
        endpoint = "/admin/groupcontent"
        header = self.headers["Admin2"]
        header2 = self.headers["fakeadmin"]

        response, data = Helpers.get_request(endpoint, header)
        response2, data2 = Helpers.get_request(endpoint, header2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 30)
        self.assertEqual(response2.status_code, 422)

    def test_create_content(self):
        endpoint = "/admin/content"
        header = self.headers["Admin1"]
        body1 = {
            "title": "Movie 1",
            "genre": "Action",
            "year": "2019"
        }
        body2 = {
            "title": "",
            "genre": "",
            "year": ""
        }

        response, data = Helpers.post_request(
            endpoint, header=header, body=body1)
        response2, data2 = Helpers.post_request(
            endpoint, header=header, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["content_id"], 31)
        self.assertEqual(response2.status_code, 400)

    def test_delete_content(self):
        selected_content = random.randrange(1, 31)
        endpoint1 = f"/admin/content/{selected_content}"
        endpoint2 = "/admin/content/31"
        header = self.headers["Admin2"]

        response, data = Helpers.delete_request(endpoint1, header=header)
        response2, data2 = Helpers.delete_request(endpoint2, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["content_id"], selected_content)
        self.assertEqual(response2.status_code, 404)
        self.assertIsNone(data2)
