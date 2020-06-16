import uuid

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class User(Model):
    class Meta:
        table_name = 'users'

    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    email = UnicodeAttribute()
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
