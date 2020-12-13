import unittest
from main import create_app, db


class TestProfiles(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()
        print("tables created")

        runner = cls.app.test_cli_runner()
        result = runner.invoke(args=["db-custom", "seed"])
        if result.exit_code != 0:
            raise ValueError(result.stdout)
        print("tables seeded")

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        print("tables dropped")
        cls.app_context.pop()

    def test_show_profiles(self):
        app = create_app()
        client = app.test_client()
        response = client.get("/profiles/")

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) == 20)
