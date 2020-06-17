from typing import List

import pytest

from tests.utils.users import User
from tests.utils.api_client import UserAPIClient
from users.models import UserModel


@pytest.fixture(scope='class')
def user_api():
    users_list: List[UserModel] = []
    user = User()

    def _user_api():
        return UserAPIClient(user=user)
    yield _user_api()

    for user_id in user.ids_list:
        try:
            user_model = UserModel.get(user_id)
            users_list.append(user_model)
        except UserModel.DoesNotExist:
            continue
    if users_list:
        for user_model in users_list:
            user_model.delete()
