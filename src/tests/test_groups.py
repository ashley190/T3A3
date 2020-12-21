import unittest
from main import create_app, db
from tests.helpers import Helpers
from models.Group_members import GroupMembers
from models.Group import Group
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

    def get_profile_ids(self, header):
        profile_ids = Helpers.get_profile_id(header)

        while len(profile_ids) == 0:
            self.tearDown()
            self.setUp()
            profile_ids = Helpers.get_profile_id(header)
        non_profile_ids = [i for i in range(1, 11) if i not in profile_ids]
        return(profile_ids, non_profile_ids)

    def generate_group_endpoints(self, header):
        profile_ids, non_profile_ids = self.get_profile_ids(header)

        endpoint1 = f"/groups/?profile_id={random.choice(profile_ids)}"
        endpoint2 = f"/groups/?profile_id={random.choice(non_profile_ids)}"
        return(endpoint1, endpoint2)

    def test_create_group(self):
        header = self.headers["test1"]
        endpoint1, endpoint2 = self.generate_group_endpoints(header)

        body1 = {
            "name": "New group",
            "description": "New netflix group with friends"
        }
        body2 = {
            "name": "",
            "description": ""
        }

        response, data = Helpers.post_request(
            endpoint1, header=header, body=body1)
        response2, data2 = Helpers.post_request(
            endpoint2, header=header, body=body1)
        response3, data3 = Helpers.post_request(
            endpoint1, header=header, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertEqual(response2.status_code, 404)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(data3["name"], ['Shorter than minimum length 1.'])

    def test_get_groups(self):
        header = self.headers["test2"]
        endpoint1, endpoint2 = self.generate_group_endpoints(header)

        response, data = Helpers.get_request(endpoint1, header=header)
        response2, data2 = Helpers.get_request(endpoint2, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertIsInstance(data, list)
        self.assertIsNone(data2)

    def test_get_group_by_id(self):
        header = self.headers["test3"]
        endpoint1 = f"/groups/{random.randrange(1, 11)}"
        endpoint2 = "/groups/31"

        response, data = Helpers.get_request(endpoint1, header=header)
        response2, data2 = Helpers.get_request(endpoint2, header=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(len(data), 4)
        self.assertIsNone(data2)

    def test_group_update(self):
        header = self.headers["test3"]
        profile_ids = Helpers.get_profile_id(header)

        groups = Helpers.get_request(
            f"/groups/?profile_id={profile_ids[0]}", header=header)
        group_ids = []
        for group in groups[1]:
            if group["admin"]:
                group_ids.append(group["groups"]["group_id"])
        non_group_ids = [i for i in range(1, 11) if i not in group_ids]

        endpoint1 = f"/groups/{group_ids[0]}?profile_id={profile_ids[0]}"
        endpoint2 = f"/groups/{non_group_ids[0]}?profile_id={profile_ids[0]}"
        body1 = {
            "name": "New group name",
            "description": "New group description"
        }
        body2 = {
            "name": "",
            "description": ""
        }

        response, data = Helpers.patch_request(endpoint1, header, body1)
        response2, data2 = Helpers.patch_request(endpoint2, header, body1)
        response3, data3 = Helpers.patch_request(endpoint1, header, body2)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response2.status_code in [401, 404])
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(data["name"], "New group name")
        self.assertEqual(data["description"], "New group description")
        self.assertIsNone(data2)
        self.assertIsInstance(data3, dict)

    def test_group_delete(self):
        header = self.headers["test4"]
        profile_ids, non_profile_ids = self.get_profile_ids(header)

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
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)

    def test_join_group(self):
        header = self.headers["test5"]
        profile_id_search = self.get_profile_ids(header)
        selected_profile_id = random.choice(profile_id_search[0])
        selected_non_profile_id = random.choice(profile_id_search[1])
        group_endpoint = f"/groups/?profile_id={selected_profile_id}"

        groups = []
        group_search = Helpers.get_request(group_endpoint, header=header)
        for group in group_search[1]:
            groups.append(group["groups"]["group_id"])

        non_groups = [i for i in range(1, 11) if i not in groups]

        body1 = {
            "profile_id": f"{selected_profile_id}"
        }
        body2 = {
            "profile_id": f"{selected_non_profile_id}"
        }

        endpoint1 = f"/groups/{non_groups[0]}/join"
        endpoint2 = f"/groups/{groups[0]}/join"

        response, data = Helpers.post_request(
            endpoint1, header=header, body=body1)
        response2, data2 = Helpers.post_request(
            endpoint2, header=header, body=body1)
        response3, data3 = Helpers.post_request(
            endpoint1, header=header, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["profile_id"], selected_profile_id)
        self.assertIsInstance(data, dict)
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)

    def test_unjoin_group(self):
        header = self.headers["test1"]
        profile_id_search = self.get_profile_ids(header)
        selected_profile_id = random.choice(profile_id_search[0])
        selected_non_profile_id = random.choice(profile_id_search[1])

        group_endpoint = f"/groups/?profile_id={selected_profile_id}"

        groups = []
        group_search = Helpers.get_request(group_endpoint, header=header)
        for group in group_search[1]:
            groups.append(group["groups"]["group_id"])

        non_groups = [i for i in range(1, 11) if i not in groups]

        body1 = {
            "profile_id": f"{selected_profile_id}"
        }
        body2 = {
            "profile_id": f"{selected_non_profile_id}"
        }

        endpoint1 = f"/groups/{groups[0]}/unjoin"
        endpoint2 = f"/groups/{non_groups[0]}/unjoin"

        response, data = Helpers.delete_request(
            endpoint1, header=header, body=body1)
        response2, data2 = Helpers.delete_request(
            endpoint2, header=header, body=body1)
        response3, data3 = Helpers.delete_request(
            endpoint1, header=header, body=body2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["profile_id"], selected_profile_id)
        self.assertEqual(data["group_id"], groups[0])
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)

    def test_remove_member(self):
        header = self.headers["test2"]
        profile_id_search = self.get_profile_ids(header)
        selected_profile_id = random.choice(profile_id_search[0])

        group = GroupMembers.query.filter_by(
            profile_id=selected_profile_id, admin=True).first()
        group_id = group.group_id
        non_group_ids = [i for i in range(1, 11) if i != group_id]

        group_members_search = GroupMembers.query.filter_by(
            group_id=group_id, admin=False)
        member_ids = []

        for group in group_members_search:
            member_ids.append(group.profile_id)

        non_member_ids = [i for i in range(1, 11) if i not in member_ids]

        endpoint1 = f"/groups/{random.choice(non_group_ids)}/remove_member"
        endpoint2 = f"/groups/{group_id}/remove_member"

        body1 = {
            "admin_id": f"{selected_profile_id}",
            "member_id": f"{random.choice(member_ids)}"
        }
        body2 = {
            "admin_id": f"{random.choice(member_ids)}",
            "member_id": f"{selected_profile_id}"
        }
        body3 = {
            "admin_id": f"{selected_profile_id}",
            "member_id": f"{random.choice(non_member_ids)}"
        }

        response, data = Helpers.delete_request(
            endpoint1, header=header, body=body1)
        response2, data2 = Helpers.delete_request(
            endpoint2, header=header, body=body2)
        response3, data3 = Helpers.delete_request(
            endpoint2, header=header, body=body3)
        response4, data4 = Helpers.delete_request(
            endpoint2, header=header, body=body1)

        self.assertTrue(response.status_code in [401, 404])
        self.assertIsNone(data)
        self.assertTrue(response2.status_code in [401, 404])
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 404)
        self.assertIsNone(data3)
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(data4["status"], "removed from group")

    def test_add_content(self):
        header = self.headers["test3"]
        profile_ids, non_profile_ids = self.get_profile_ids(header)

        group_search = GroupMembers.query.filter_by(profile_id=profile_ids[0])

        group_ids = []
        for group in group_search:
            group_ids.append(group.groups.group_id)

        non_group_ids = [i for i in range(1, 11)if i not in group_ids]

        group_content_ids = []
        group_content_search = Group.query.get(group_ids[0])
        for content in group_content_search.content:
            group_content_ids.append(content.content_id)

        non_group_content_ids = [i for i in range(
            1, 31) if i not in group_content_ids]

        endpoint1 = f"/groups/{group_ids[0]}/content?profile_id={profile_ids[0]}"       # noqa: E501
        endpoint2 = f"/groups/{non_group_ids[0]}/content?profile_id={profile_ids[0]}"   # noqa: E501

        body1 = {
            "content_id": f"{non_group_content_ids[0]}"
        }
        body2 = {
            "content_id": f"{random.choice(group_content_ids)}"
        }
        body3 = {
            "content_id": "31"
        }

        response, data = Helpers.post_request(
            endpoint1, header=header, body=body1)
        data_content = []
        for content in data["groups"]["content"]:
            data_content.append(content["content_id"])
        response2, data2 = Helpers.post_request(
            endpoint2, header=header, body=body1)
        response3, data3 = Helpers.post_request(
            endpoint1, header=header, body=body2)
        response4, data4 = Helpers.post_request(
            endpoint1, header=header, body=body3)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(non_group_content_ids[0] in data_content)
        self.assertEqual(response2.status_code, 401)
        self.assertIsNone(data2)
        self.assertEqual(response3.status_code, 401)
        self.assertIsNone(data3)
        self.assertEqual(response4.status_code, 404)
        self.assertIsNone(data4)
