import pytest


class TestCRUDUsers:
    def test_valid_data_for_create_users(self, user_api):
        response = user_api.create_user()
        assert response.status_code == 201

    def test_invalid_data_for_create_users(self, user_api):
        user_api.user.email = 'asdasd'
        response = user_api.create_user()
        assert response.status_code == 400

    def test_valid_data_for_patch_user(self, user_api):
        response = user_api.patch_user(json_data={'first_name': 'lalala'})
        assert response.status_code == 200

    def test_invalid_data_for_patch_user(self, user_api):
        response = user_api.patch_user(json_data={'email': 'lololo'})
        assert response.status_code == 400

    def test_get_user(self, user_api):
        response = user_api.get_user()
        assert response.status_code == 200

    def test_get_users(self, user_api):
        response = user_api.get_users()
        assert response.status_code == 200

    def test_delete_existent_user(self, user_api):
        response = user_api.delete_user()
        assert response.status_code == 204

    def test_delete_nonexistent_user(self, user_api):
        user_api.user.id_dynamodb = 'nonexisted'
        response = user_api.delete_user()
        assert response.status_code == 404
