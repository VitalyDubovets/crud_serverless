from dataclasses import dataclass, field

import requests
from decouple import config
from requests import Response

from .users import User


@dataclass
class UserAPIClient:
    user: User = field(default_factory=User())
    stage: str = field(default=config('stage', 'dev'))
    domain: str = field(default=config('DOMAIN'))
    api_version: str = 'v1'

    @property
    def url(self) -> str:
        return f'https://{self.domain}/{self.stage}/api/{self.api_version}/users'

    def create_user(self, method: str = 'POST') -> Response:
        response: Response = requests.request(method=method, url=self.url, json=self.user.request_params)
        if response.status_code == 201:
            user_id = response.json()['user']['id']
            self.user.id_dynamodb = user_id
            self.user.ids_list.append(user_id)
        return response

    def patch_user(self, json_data: dict, method: str = 'PATCH') -> Response:
        url: str = self.url + f'/{self.user.id_dynamodb}'
        return requests.request(method=method, url=url, json=json_data)

    def get_user(self) -> Response:
        url: str = self.url + f'/{self.user.id_dynamodb}'
        return requests.request(method='GET', url=url)

    def get_users(self) -> Response:
        return requests.request(method='GET', url=self.url)

    def delete_user(self) -> Response:
        url: str = self.url + f'/{self.user.id_dynamodb}'
        return requests.request(method='DELETE', url=url)
