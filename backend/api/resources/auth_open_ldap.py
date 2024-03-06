import time

from flask_restful import Resource, request, abort

from backend.api.common.crypt_passwd import CryptPasswd
from backend.api.common.decorators import define_schema
from backend.api.common.managers_ldap.connection_ldap_manager import ConnectionManagerLDAP
from backend.api.common.managers_ldap.group_ldap_manager import GroupManagerLDAP
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.route import Route
from backend.api.common.token_manager import TokenManagerDB
from backend.api.common.managers_ldap.authentication_ldap_manager import AuthenticationManagerLDAP
from backend.api.common.user_manager import UserLdap
from backend.api.config import settings
from backend.api.redis.redis_storage import RedisStorage
from backend.api.resources.schema import AuthSchemaLdapCreate, TokenSchemaLdap


class AuthOpenLDAP(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer = CommonSerializer()
        self.connection = None
        self.route = Route.AUTH

    @define_schema
    def post(self, *args, **kwargs):  # pass and uid (it is part of the dn) check ldap.
        """
        This function confirms the args username and password,
        then performs authentication, if authentication is successful
        token is sent user, else error 401.
        """
        start1 = time.perf_counter()
        schema = kwargs['schema']

        sum_time = 0

        start = time.perf_counter()
        json_data = request.get_json()
        deserialized_data = self.serializer.deserialize_data(schema, json_data)
        end = time.perf_counter()
        print(f'Time of work deseriaz : {(end - start):.4f}s')
        sum_time += end - start
        user = UserLdap(**deserialized_data)

        start = time.perf_counter()
        with ConnectionManagerLDAP(user) as connection:
            connection.connect()
            end = time.perf_counter()
            print(f'Time of work connnnnn : {(end - start):.4f}s')

            start = time.perf_counter()
            ldap_auth = AuthenticationManagerLDAP(user, connection)
            user = ldap_auth.authenticate()
            end = time.perf_counter()
            print(f'Time of work conn : {(end - start):.4f}s')
            sum_time += end - start

            # start = time.perf_counter()
            # print('redis', RedisStorage().get('ggg'))
            # end = time.perf_counter()
            # print(f'Time of work redis : {(end - start):.4f}s')

            start = time.perf_counter()
            group = GroupManagerLDAP(connection=connection).get_webadmins_group()
            user.is_webadmin = UserManagerLDAP(connection=connection).is_webadmin(user.dn, group)
            end = time.perf_counter()
            print(f'Time of work define group : {(end - start):.4f}s')
            sum_time += end - start

        if user.is_webadmin: user.role = Role.WEB_ADMIN
        else: user.role = Role.SIMPLE_USER

        # connection.close()

        start = time.perf_counter()
        user.userPassword = CryptPasswd(
            password=deserialized_data['userPassword'].encode(),
            secret_key=bytes(settings.SECRET_KEY.encode())
        ).crypt()
        end = time.perf_counter()
        print(f'Time of work crypt : {(end - start):.4f}s')
        sum_time += end - start

        start = time.perf_counter()
        token = TokenManagerDB(user=user).create_token()
        end = time.perf_counter()
        print(f'Time of work db : {(end - start):.4f}s')
        sum_time += end - start

        if not token:
            abort(400, message='Try again now or later', status=400)

        start = time.perf_counter()
        serialized_data = self.serializer.serialize_data(
            TokenSchemaLdap.__name__, {'token': token, 'uid': user.uid, 'role': user.role.value}
        )
        end = time.perf_counter()
        print(f'Time of work seriaz : {(end - start):.4f}s')
        sum_time += end - start
        print('sum-time', sum_time)

        end1 = time.perf_counter()
        print(f'Time of work com : {(end1 - start1):.4f}s')
        return serialized_data, 200
