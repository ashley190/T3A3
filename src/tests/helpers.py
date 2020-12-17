from main import create_app


class Helpers():
    app = create_app()
    client = app.test_client()

    @classmethod
    def post_request(cls, endpoint, header=None, body=None):
        response = cls.client.post(endpoint, headers=header, json=body)
        data = response.get_json()
        return (response, data)

    @classmethod
    def get_request(cls, endpoint, header=None):
        response = cls.client.get(endpoint, headers=header)
        data = response.get_json()
        return (response, data)

    @classmethod
    def patch_request(cls, endpoint, header, body):
        response = cls.client.patch(endpoint, headers=header, json=body)
        data = response.get_json()
        return (response, data)

    @classmethod
    def put_request(cls, endpoint, header, body):
        response = cls.client.put(endpoint, headers=header, json=body)
        data = response.get_json()
        return (response, data)

    @classmethod
    def delete_request(cls, endpoint, header=None, body=None):
        response = cls.client.delete(endpoint, headers=header, json=body)
        data = response.get_json()
        return (response, data)

    @classmethod
    def get_profile_id(cls, header):
        profile_ids = []
        response, data = Helpers.get_request("/profiles/", header=header)
        for profile in data:
            profile_ids.append(profile["profile_id"])
        return profile_ids
