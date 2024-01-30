from flask_restful import Resource, request, abort

from backend.api.common.roles import Role
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.token_manager import TokenManager
from backend.api.common.managers_ldap.authentication_ldap_manager import AuthenticationManagerLDAP
from backend.api.common.user_manager import UserLdap
from backend.api.resources.schema import AuthUserSchemaLdap, TokenSchemaLdap


class AuthOpenLDAP(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer = CommonSerializer()

    def post(self):  # pass and uid (it is part of the dn) check ldap.
        """
        This function confirms the args username and password,
        then performs authentication, if authentication is successful
        token is sent user, else error 403.
        """
        json_data = request.get_json()

        deserialized_data = self.serializer.deserialize_data(AuthUserSchemaLdap.__name__, json_data)

        user = UserLdap(**deserialized_data)
        ldap_auth = AuthenticationManagerLDAP(user)
        response = ldap_auth.authenticate()

        if response.status.value == 1:
            abort(401, message='Invalid username or password.')

        ldap_auth.user.dn = response.user_dn
        ldap_auth.create_connection_new()
        ldap_auth.connect_new()
        ldap_auth.show_connections()

        user.dn = response.user_dn
        user.uid = response.user_id

        user.is_webadmin = ldap_auth.is_webadmin(user.dn)
        if user.is_webadmin: user.role = Role.WEBADMIN
        else: user.role = Role.SIMPLE_USER

        ldap_auth.close()

        token = TokenManager(user=user).create_token()

        serialized_data = self.serializer.serialize_data(
            TokenSchemaLdap.__name__, {'token': token, 'uid': user.uid}
        )

        return serialized_data, 200
