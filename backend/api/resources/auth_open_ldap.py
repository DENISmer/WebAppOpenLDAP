from flask_restful import Resource, request, abort

from backend.api.common.crypt_passwd import CryptPasswd
from backend.api.common.managers_ldap.connection_ldap_manager import ConnectionManagerLDAP
from backend.api.common.managers_ldap.group_ldap_manager import GroupManagerLDAP
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.token_manager import TokenManagerDB
from backend.api.common.managers_ldap.authentication_ldap_manager import AuthenticationManagerLDAP
from backend.api.common.user_manager import UserLdap
from backend.api.resources.schema import AuthUserSchemaLdap, TokenSchemaLdap


class AuthOpenLDAP(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer = CommonSerializer()
        self.connection = None

    # @connection_ldap
    def post(self, *args, **kwargs):  # pass and uid (it is part of the dn) check ldap.
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
            abort(401, message='Invalid username or password', status=401)

        user.dn = response.user_dn
        user.uid = response.user_id

        connection = ConnectionManagerLDAP(user)
        connection.connect()

        group = GroupManagerLDAP(connection=connection).get_webadmins_group()
        user.is_webadmin = UserManagerLDAP(connection=connection).is_webadmin(user.dn, group)

        if user.is_webadmin: user.role = Role.WEBADMIN
        else: user.role = Role.SIMPLE_USER

        connection.close()

        user.userPassword = CryptPasswd(password=deserialized_data['userPassword'].encode()).crypt()
        token = TokenManagerDB(user=user).create_token()
        if not token:
            abort(400, message='Try again now or later', status=400)

        serialized_data = self.serializer.serialize_data(
            TokenSchemaLdap.__name__, {'token': token, 'uid': user.uid, 'role': user.role.value}
        )

        return serialized_data, 200
