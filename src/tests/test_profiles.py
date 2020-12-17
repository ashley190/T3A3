import unittest
from main import create_app, db
from tests.helpers import Helpers
import random


class TestProfiles(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        result = runner.invoke(args=["db-custom", "seed"])
        if result.exit_code != 0:
            raise ValueError(result.stdout)

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

    def test_show_profiles(self):
        endpoint = "/profiles/"
        response, data = Helpers.get_request(
            endpoint, header=self.headers["test1"])
        response2, data2 = Helpers.get_request(
            endpoint, header=self.headers["fakeuser"])

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(response2.status_code, 422)

    def test_create_profile(self):
        endpoint = "/profiles/create"
        body = {
            "name": "New profile",
            "restrictions": "M"
        }
        body2 = {
            "name": "New profile",
            "restrictions": "A"
        }
        response, data = Helpers.post_request(
            endpoint, body=body, header=self.headers["test3"])
        response2, data2 = Helpers.post_request(
            endpoint, body=body2, header=self.headers["test4"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["profile_id"], 11)
        self.assertEqual(data["name"], "New profile")
        self.assertEqual(data["restrictions"], "M")

    def test_get_profile_by_id(self):
        header = self.headers["test2"]
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)

        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]

        endpoint1 = f"/profiles/{profile_ids[0]}"
        endpoint2 = f"/profiles/{non_profile_ids[0]}"
        response, data = Helpers.get_request(endpoint1, header=header)
        response2, data2 = Helpers.get_request(endpoint2, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(data["user"]["email"], "test2@test.com")
        self.assertIsNone(data2)

    def test_delete_profile(self):
        header = self.headers["test3"]
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)

        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]

        endpoint1 = f"/profiles/{profile_ids[0]}"
        endpoint2 = f"/profiles/{non_profile_ids[0]}"
        response, data = Helpers.delete_request(endpoint1, header=header)
        response2, data2 = Helpers.delete_request(endpoint2, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(data["user"]["user_id"], 3)
        self.assertIsNone(data2)

    def test_unrecommended_content(self):
        header = self.headers["test4"]
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)

        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]
        endpoint1 = f"/profiles/{profile_ids[0]}/unrecommend"
        endpoint2 = f"/profiles/{non_profile_ids[0]}/unrecommend"
        response, data = Helpers.get_request(endpoint1, header=header)
        response2, data2 = Helpers.get_request(endpoint2, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(len(data), 2)
        self.assertIsNone(data2)

    def test_unrecommend_content(self):
        header = self.headers["test4"]
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)
        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]

        endpoint1 = f"/profiles/{profile_ids[0]}/unrecommend"
        endpoint2 = f"/profiles/{non_profile_ids[0]}/unrecommend"

        get_content = Helpers.get_request(endpoint1, header=header)
        unrecommended = []
        for content in get_content[1]:
            unrecommended.append(content["content_id"])

        available_content = [i for i in range(1, 31) if i not in unrecommended]
        body1 = {
            "content_id": random.choice(available_content)
        }
        body2 = {
            "content_id": 31
        }
        response, data = Helpers.put_request(
            endpoint1, header=header, body=body1)
        response2, data2 = Helpers.put_request(
            endpoint2, header=header, body=body1)
        response3, data3 = Helpers.put_request(
            endpoint1, header=header, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(response2.status_code, 404)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)

    def test_remove_content(self):
        header = self.headers["test5"]
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)
        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]

        endpoint1 = f"/profiles/{profile_ids[0]}/unrecommend"
        endpoint2 = f"/profiles/{non_profile_ids[0]}/unrecommend"

        get_content = Helpers.get_request(endpoint1, header=header)
        unrecommended = []
        for content in get_content[1]:
            unrecommended.append(content["content_id"])

        available_content = [i for i in range(1, 31) if i not in unrecommended]
        body1 = {
            "content_id": random.choice(unrecommended)
        }
        body2 = {
            "content_id": random.choice(available_content)
        }

        response, data = Helpers.delete_request(
            endpoint1, header=header, body=body1)
        response2, data2 = Helpers.delete_request(
            endpoint2, header=header, body=body1)
        response3, data3 = Helpers.delete_request(
            endpoint1, header=header, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(response2.status_code, 404)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)
