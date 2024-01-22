import pprint

from flask_restful import Resource, marshal_with, fields, reqparse, abort, request
from marshmallow import ValidationError

from backend.api.common.auth_http_token import auth
from backend.api.common.decorators import connection_ldap, permission_user
from backend.api.common.ldap_manager import UserManagerLDAP
from backend.api.common.user_manager import User
from backend.api.config.fields import simple_user_fields, webadmins_fields, search_fields
from backend.api.common.roles import Role
from backend.api.resources import schema


# resource_fields = {
#     'dn': fields.String,
#     'uidNumber': fields.Integer,
#     'gidNumber': fields.Integer,
#     'uid': fields.List(fields.String),
#     'sshPublicKey': fields.List(fields.String),
#     'st': fields.List(fields.String),
#     'mail': fields.List(fields.String),
#     'street': fields.List(fields.String),
#     'cn': fields.List(fields.String),
#     'displayName': fields.List(fields.String),
#     'givenName': fields.List(fields.String),
#     'sn': fields.List(fields.String),
#     'postalCode': fields.List(fields.Integer),
#     'homeDirectory': fields.String,
#     'loginShell': fields.String,
#     'objectClass': fields.List(fields.String),
# }
# resource_fields_list = {
#     'users': fields.List(
#         fields.Nested(resource_fields)
#     ),
#     'fields': fields.List(fields.String),
# }
#
# parser_post = reqparse.RequestParser()
# parser_put = reqparse.RequestParser()
# parser_patch = reqparse.RequestParser()
# for key, value in webadmins_fields['fields'].items():
#     parser_post.add_argument(
#         key, type=value['element_type'], required=True,
#         action='append' if value['type'] else None
#     )
#     parser_put.add_argument(
#         key, type=value['element_type'],
#         required=True if 'update' in value['operation']
#                          and 'userPassword' != key else False,
#         action='append' if value['type'] else 'store'
#     )
#     parser_patch.add_argument(
#         key, type=value['element_type'],
#         action='append' if value['type'] else 'store'
#     )
#
# parser_get_list = reqparse.RequestParser()
# parser_get_list.add_argument('search', location='values')


@auth.get_user_roles  # roles
def get_user_roles(user):
    return Role(user['role'])


@auth.error_handler
def auth_error(status):
    return {'message': 'Unauthorized Access'}, status


class UserOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_manager_ldap: UserManagerLDAP = None

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    # @marshal_with(resource_fields)
    @connection_ldap
    @permission_user
    def get(self, username_uid, *args, **kwargs):
        user = self._user_manager_ldap.get_user(username_uid)
        user_schema = kwargs['user_schema']
        serialized_user = getattr(schema, user_schema)().dump(user)

        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    # @marshal_with(resource_fields)
    @connection_ldap
    @permission_user
    def put(self, username_uid, *args, **kwargs):

        deserialized_user = {}
        json_data = request.get_json()

        user_schema = kwargs['user_schema']
        user_fields = kwargs['user_fields']
        print('user_schema', user_schema)
        try:
            deserialized_user = getattr(schema, user_schema)().load(json_data, partial=False)
            print('user', deserialized_user)
        except ValidationError as e:
            abort(400, message=e.messages)

        user = User(username_uid=username_uid, **deserialized_user)
        self._user_manager_ldap.modify_user(
            user=user,
            fields=user_fields['fields'],
            operation='update'
        )
        serialized_user = getattr(schema, user_schema)().dump(user)
        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    # @marshal_with(resource_fields)
    @connection_ldap
    @permission_user
    def patch(self, username_uid, *args, **kwargs):
        deserialized_user = {}
        json_data = request.get_json()
        user_schema = kwargs['user_schema']
        user_fields = kwargs['user_fields']

        try:
            deserialized_user = getattr(schema, user_schema)().load(json_data, partial=True)
        except ValidationError as e:
            abort(400, message=e.messages)

        user = User(username_uid=username_uid, **deserialized_user)
        # self._user_manager_ldap.close_connection()

        self._user_manager_ldap.modify_user(
            user=user,
            fields=user_fields['fields'],
            operation='update'
        )

        serialized_user = getattr(schema, user_schema)().dump(user)
        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_user
    def delete(self, username_uid):
        print('DELETE', username_uid)
        user = User(username_uid=username_uid)

        result = self._user_manager_ldap.delete_user(user)
        if not result:
            abort(400)

        return None, 204


class UserListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user_manager_ldap: UserManagerLDAP = None

    @auth.login_required(role=[Role.WEBADMIN])
    # @marshal_with(resource_fields_list)
    @connection_ldap
    @permission_user
    def get(self, *args, **kwargs):
        user_schema = kwargs['user_schema']

        search = request.args.get('search')
        if search and str(search).isdigit():
            search = int(search)

        users = self._user_manager_ldap.get_users(
            value=search, ####
            fields=search_fields, ####
            attributes=['uid', 'cn', 'sn'],
            required_fields={'objectClass': 'person'},
        )
        serialized_users = getattr(schema, user_schema)().dump(users, many=True)

        return {'users': serialized_users}, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_user
    def post(self, *args, **kwargs):
        json_data = request.get_json()

        deserialized_user = {}
        user_schema = kwargs['user_schema']
        user_fields = kwargs['user_fields']

        try:
            deserialized_user = getattr(schema, user_schema)().load(json_data, partial=False)
            print('user', deserialized_user)
        except ValidationError as e:
            abort(400, message=e.messages)

        user = User(**deserialized_user)
        self._user_manager_ldap.create_user( ##### must done #####
            user=user, ##### must done #####
            fields=user_fields['fields'], ##### must done #####
            operation='create' ##### must done #####
        ) ##### must done #####
        return user, 201
