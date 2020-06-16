from marshmallow import Schema, fields, post_load

from users.models import User


class UserSchemaCreate(Schema):
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class UserSchemaPatch(Schema):
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()


class UserSchemaGet(Schema):
    id = fields.Str(required=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name')
        ordered = True
