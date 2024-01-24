from flask_restful import Resource, fields, marshal_with, request, reqparse, abort

from marshmallow import ValidationError

from backend.api.common.roles import Role
from backend.api.common.token_manager import TokenManager, Token
from backend.api.common.authentication_ldap import AuthenticationLDAP
from backend.api.common.user_manager import UserLdap
from backend.api.resources.schema import AuthUserSchemaLdap, TokenSchemaLdap


class AuthOpenLDAP(Resource):

    def post(self):  # pass and uid (it is part of the dn) check ldap.
        """
        This function confirms the args username and password,
        then performs authentication, if authentication is successful
        token is sent user, else error 403.
        """
        deserialized_data = {}
        json_data = request.get_json()

        try:
            deserialized_data = AuthUserSchemaLdap().load(json_data)
        except ValidationError as e:
            abort(400, message=e.messages)

        user = UserLdap(**deserialized_data)
        ldap_auth = AuthenticationLDAP(user)
        response = ldap_auth.authenticate()

        if response.status.value == 1:
            abort(401, message='Invalid username or password.')

        ldap_auth.connect()

        user.dn = response.user_dn
        user.uid = response.user_id
        user.is_webadmin = ldap_auth.is_webadmin(user.dn)
        if user.is_webadmin:
            user.role = Role.WEBADMIN

        ldap_auth.close_connection()

        token = TokenManager(user=user).create_token()
        serialized_data = TokenSchemaLdap().dump({'token': token})

        return serialized_data, 200
