import unittest
from main import create_app, db
from tests.helpers import Helpers
import random


class TestGroups(unittest.TestCase):
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

    def generate_group_endpoints(self, header):
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)
        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]

        endpoint1 = f"/groups/?profile_id={random.choice(profile_ids)}"
        endpoint2 = f"/groups/?profile_id={random.choice(non_profile_ids)}"
        return(endpoint1, endpoint2)

    # def test_create_group(self):
    #     header = self.headers["test1"]
    #     endpoint1, endpoint2 = self.generate_group_endpoints(header)

    #     body1 = {
    #         "name": "New group",
    #         "description": "New netflix group with friends"
    #     }
    #     body2 = {
    #         "name": "",
    #         "description": ""
    #     }

    #     response, data = Helpers.post_request(
    #         endpoint1, header=header, body=body1)
    #     response2, data2 = Helpers.post_request(
    #         endpoint2, header=header, body=body1)
    #     response3, data3 = Helpers.post_request(
    #         endpoint1, header=header, body=body2)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(data, dict)
    #     self.assertEqual(response2.status_code, 404)
    #     self.assertIsNone(data2)
    #     self.assertEqual(response3.status_code, 400)
    #     self.assertEqual(data3["name"], ['Shorter than minimum length 1.'])

    # def test_get_groups(self):
    #     header = self.headers["test2"]
    #     endpoint1, endpoint2 = self.generate_group_endpoints(header)

    #     response, data = Helpers.get_request(endpoint1, header=header)
    #     response2, data2 = Helpers.get_request(endpoint2, header=header)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response2.status_code, 404)
    #     self.assertIsInstance(data, list)
    #     self.assertIsNone(data2)

    # def test_get_group_by_id(self):
    #     header = self.headers["test3"]
    #     endpoint1 = f"/groups/{random.randrange(1, 11)}"
    #     endpoint2 = "/groups/31"

    #     response, data = Helpers.get_request(endpoint1, header=header)
    #     response2, data2 = Helpers.get_request(endpoint2, header=header)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response2.status_code, 404)
    #     self.assertEqual(len(data), 4)
    #     self.assertIsNone(data2)

    # def test_group_update(self):
    #     header = self.headers["test3"]
    #     profile_ids = Helpers.get_profile_id(header)

    #     groups = Helpers.get_request(
    #         f"/groups/?profile_id={profile_ids[0]}", header=header)
    #     group_ids = []
    #     for group in groups[1]:
    #         if group["admin"]:
    #             group_ids.append(group["groups"]["group_id"])
    #     non_group_ids = [i for i in range(1, 11) if i not in group_ids]

    #     endpoint1 = f"/groups/{group_ids[0]}?profile_id={profile_ids[0]}"
    #     endpoint2 = f"/groups/{non_group_ids[0]}?profile_id={profile_ids[0]}"
    #     body1 = {
    #         "name": "New group name",
    #         "description": "New group description"
    #     }
    #     body2 = {
    #         "name": "",
    #         "description": ""
    #     }

    #     response, data = Helpers.patch_request(endpoint1, header, body1)
    #     response2, data2 = Helpers.patch_request(endpoint2, header, body1)
    #     response3, data3 = Helpers.patch_request(endpoint1, header, body2)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response2.status_code, 404)
    #     self.assertEqual(response3.status_code, 400)
    #     self.assertEqual(data["name"], "New group name")
    #     self.assertEqual(data["description"], "New group description")
    #     self.assertIsNone(data2)
    #     self.assertIsInstance(data3, dict)

    def test_group_delete(self):
        header = self.headers["test4"]
        profile_ids = Helpers.get_profile_id(header)
        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]

        groups = Helpers.get_request(
            f"/groups/?profile_id={profile_ids[0]}", header=header)
        group_ids = []
        for group in groups[1]:
            if group["admin"]:
                group_ids.append(group["groups"]["group_id"])
        non_group_ids = [i for i in range(1, 11) if i not in group_ids]

        endpoint1 = f"/groups/{group_ids[0]}?profile_id={profile_ids[0]}"
        endpoint2 = f"/groups/{non_group_ids[0]}?profile_id={profile_ids[0]}"
        endpoint3 = f"/groups/{group_ids[0]}?profile_id={non_profile_ids[0]}"

        response, data = Helpers.delete_request(endpoint1, header=header)
        response2, data2 = Helpers.delete_request(endpoint2, header=header)
        response3, data3 = Helpers.delete_request(endpoint3, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(response2.status_code, 404)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)
