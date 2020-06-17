import json
import logging

import marshmallow

from users.models import UserModel
from users.schemas import UserSchemaCreate, UserSchemaPatch, UserSchemaGet


logger = logging.getLogger('user_logs')


class UserAPI:
    @classmethod
    def post(cls, event: dict, context) -> dict:
        logger.info('Starting to create a user')
        if event.get('body'):
            try:
                user: UserModel = UserSchemaCreate().loads(event.get('body'))
                user.save()
                response: dict = {
                    'statusCode': 201,
                    'body': json.dumps({
                        'message': 'User was created successful',
                        'user': UserSchemaGet().dump(user)
                    })
                }
                logger.info('User created successful')
            except marshmallow.exceptions.ValidationError as err:
                response: dict = {
                    'statusCode': 400,
                    'body': json.dumps(
                        err.messages
                    )
                }
                logger.warning('Invalid data')
        else:
            response: dict = {
                'statusCode': 400,
                'body': json.dumps("Request body is empty")
            }
            logger.error("Request body is empty")
        return response

    @classmethod
    def patch(cls, event: dict, context) -> dict:
        logger.info('Starting to patch a user')
        if event.get('body'):
            user_id: str = event.get('pathParameters').get('user_id')
            try:
                user: UserModel = UserModel.get(user_id)
                patch_partial_params: dict = UserSchemaPatch(unknown=marshmallow.EXCLUDE).loads(event.get('body'))
                user.update(actions=[
                    getattr(UserModel, attr).set(value) for attr, value in patch_partial_params.items()
                ])
                response: dict = {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'User was patched successful',
                        'user': UserSchemaGet().dump(UserModel.get(user_id))
                    })
                }
                logger.info('User was patched successful')
            except UserModel.DoesNotExist:
                response: dict = {
                    'statusCode': 404,
                    'body': json.dumps({
                        'message': json.dumps('User does not exist'),
                    })
                }
                logger.info('User does not exist')
            except marshmallow.exceptions.ValidationError as err:
                response: dict = {
                    'statusCode': 400,
                    'body': json.dumps(
                        err.messages
                    )
                }
                logger.warning('Invalid data')
        else:
            response: dict = {
                'statusCode': 400,
                'body': json.dumps('Request body is empty')
            }
            logger.error('Request body is empty')
        return response

    @classmethod
    def get(cls, event: dict, context) -> dict:
        user_id: str = event.get('pathParameters').get('user_id')
        try:
            user: UserModel = UserModel.get(user_id)
            response: dict = {
                'statusCode': 200,
                'body': json.dumps(UserSchemaGet().dump(user))
            }
        except UserModel.DoesNotExist:
            response: dict = {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'User not found'
                })
            }
        return response

    @classmethod
    def delete(cls, event: dict, context) -> dict:
        user_id: str = event.get('pathParameters').get('user_id')
        try:
            user: UserModel = UserModel.get(user_id)
            deleted_user: dict = UserSchemaGet().dump(user)
            user.delete()
            response: dict = {
                'statusCode': 204,
                'body': json.dumps({
                    'message': 'User was deleted successful',
                    'user': deleted_user
                })
            }
        except UserModel.DoesNotExist:
            response: dict = {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'User not found'
                })
            }
        return response

    @classmethod
    def get_list(cls, event, context):
        limit = 0
        if event.get('queryStringParameters'):
            limit_str = event.get('queryStringParameters').get('limit')
            limit = int(limit_str) if limit_str else limit
        users = [item for item in UserModel.scan()]
        users_map = list(map(UserSchemaGet().dump, users))
        response = {
            'statusCode': 200,
            'body': json.dumps(
                users_map[0:limit] if limit else users_map[0:1000]
            )
        }
        return response


create_user = UserAPI.post
patch_user = UserAPI.patch
get_user = UserAPI.get
get_users = UserAPI.get_list
delete_user = UserAPI.delete
