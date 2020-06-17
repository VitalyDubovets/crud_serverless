from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    id_dynamodb: str = None
    email: str = field(default='example@test-gmail.com')
    first_name: str = field(default='first_name')
    last_name: str = field(default='last_name')
    ids_list: List[str] = field(default_factory=list)

    @property
    def request_params(self) -> dict:
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
