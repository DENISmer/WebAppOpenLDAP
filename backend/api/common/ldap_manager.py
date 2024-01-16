import pprint
import time
import orjson
import ssl

from flask_ldap3_login import LDAP3LoginManager

from ldap3 import Tls, ALL_ATTRIBUTES, Connection, MODIFY_REPLACE

from backend.api.common.user_manager import User
from backend.api.config.fields import search_fields
from backend.api.config.ldap import config


class LDAPManager(LDAP3LoginManager): # Singleton
    _instance = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_config(config)
        self.tls_ctx = None
        self._add_tls_ctx()

        for host in config['LDAP_HOSTS']:
            self.add_server(host, config['LDAP_PORT'], use_ssl=config['LDAP_USE_SSL'], tls_ctx=self.tls_ctx)

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(LDAPManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance[cls]

    def _add_tls_ctx(self):
        if config['LDAP_USE_SSL']:
            self.tls_ctx = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1, ca_certs_file=config['CERT_PATH'])


class InitLdap:
    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        self.ldap_manager = LDAPManager()


class AuthenticationLDAP(InitLdap):

    def authenticate(self):
        response = self.ldap_manager.authenticate(username=self.user.username_uid, password=self.user.userPassword)
        return response  # *.status: 2 - success, 1 - failed


class ConnectionLDAP(InitLdap):

    _connections = {}

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(user, args, kwargs)
        self._connection = None

    def show_connections(self):
        print('connection - ', self._connection.usage)
        for key, value in self._connections.items():
            print(f'key: {key}, value: , closed: {value._connection.closed}, listening: {value._connection.listening}')

    def connect(self):
        """
        This function performs connection to OpenLDAP server
        :return: None
        """
        self._connection: Connection = self._connections.get(self.user.username_uid)

        if not self._connection:
            conn_result = True
        else:
            conn_result = self._connection.closed or not self._connection.listening

        if conn_result:
            self._connection = self.ldap_manager.make_connection(
                bind_user=self.user.username_uid,
                bind_password=self.user.userPassword,
            )
            self._connection.open()

            if config['LDAP_USE_SSL']:
                self._connection.tls_started()
                self._connection.bind()

            self._connections[self.user.username_uid] = self._connection

    def get_connection(self):
        return self._connection

    def close(self):
        """
        This function performs close connection
        :return: None
        """
        self._connection.unbind()

    def search(self, value, fields, attributes=ALL_ATTRIBUTES):
        status_search = self._connection.search(
            search_base='dc=example,dc=com',
            search_filter='(|%s)' % "".join([f'({field}={fields[field] % value})' for field in fields]),
            attributes=attributes
        )
        if not status_search:
            return []
        return self._connection.entries

    def get_user(self, uid, attributes=ALL_ATTRIBUTES):
        status_search = self._connection.search(
            'dc=example,dc=com',
            f'(uid={uid})',
            attributes=attributes
        )

        data_json = {}
        if not status_search:
            return data_json

        data = self._connection.entries[0].entry_to_json()
        data_json.update(orjson.loads(data))

        return data_json

    def create_user(self, user: User):
        dn = user.dn

        del user.__dict__['dn']
        self._connection.add(
            dn,
            attributes=user.__dict__
        )
        print('result: ', self._connection.result)

    def modify_user(self, user: User):
        data_user = self.get_user(user.username_uid, attributes=['mail'])
        print('data_user', data_user)

        print({
            key: [(MODIFY_REPLACE, [value])]
            for key, value in user.__dict__.items() if value
        })

        # if data_user:
        #     user.dn = data_user['dn']
        #     user_dn = user.dn
        #     del user.__dict__['dn']
        #     del user.__dict__['username_uid']
        #     self._connection.modify(
        #         user_dn,
        #         {
        #             key: [(MODIFY_REPLACE, [value])]
        #             for key, value in user.__dict__.items() if value
        #         }
        #     )
        # return user
        return user

    def delete_user(self, user: User):
        data_user = self.get_user(user.username_uid, attributes=[])
        if not data_user:
            return False

        user.dn = data_user['dn']
        self._connection.delete(user.dn)
        return True

    def get_users(self):
        pass

    def get_groups(self):
        pass

    def is_webadmin(self):
        pass


# connection = ConnectionLDAP(User(uid='bob', userPassword='bob'))
# connection.connect()
#
# print('__test__')
# print(connection.search('5000', fields=search_fields))
# print('_0_')
# connection.show_connections()
#
# # time.sleep(11)
#
# print('_0_')
# connection.show_connections()
# print('search _0_:', connection.get_user(uid='bob'))
#
# connection1 = ConnectionLDAP(User(uid='john', userPassword='john'))
# connection1.connect()
#
# time.sleep(5)
#
# connection.close()
# print('_1_')
# connection1.show_connections()
# # print('search _1_:', connection1.get_user(uid='john'))
# print('_0_')
# connection1.close()
# connection1.show_connections()
