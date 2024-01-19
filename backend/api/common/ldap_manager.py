import pprint
import time
from typing import Dict

import orjson
import ssl

from flask_ldap3_login import LDAP3LoginManager
from flask import abort

from ldap3 import Tls, ALL_ATTRIBUTES, Connection, MODIFY_REPLACE, EXTERNAL
from ldap3.core.exceptions import LDAPInsufficientAccessRightsResult

from backend.api.common.groups import Group
from backend.api.common.user_manager import User
from backend.api.config.ldap import config


class LDAPManager(LDAP3LoginManager):  # Singleton
    _instance = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_config(config)
        self.tls_ctx = None
        self._add_tls_ctx()

        for host in config['LDAP_HOSTS']:
            self.add_server(
                hostname=host,
                port=config['LDAP_PORT'],
                use_ssl=config['LDAP_USE_SSL'],
                tls_ctx=self.tls_ctx,
            )

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(LDAPManager, cls) \
                .__new__(cls, *args, **kwargs)
        return cls._instance[cls]

    def _add_tls_ctx(self):
        if config['LDAP_USE_SSL']:
            self.tls_ctx = Tls(
                validate=ssl.CERT_REQUIRED,
                version=ssl.PROTOCOL_TLSv1,
                ca_certs_file=config['CERT_PATH']
            )


class ConnectionLDAP:
    _connections = {}

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        self.ldap_manager = LDAPManager()
        self._connection = None

    def connect(self):
        """
        This function performs connection to OpenLDAP server
        :return: None
        """
        self._connection: Connection = self._connections.get(
            self.user.get_username_uid()
        )

        if not self._connection:
            conn_result = True
        else:
            conn_result = self._connection.closed or not self._connection.listening

        if conn_result:
            self._connection = self.ldap_manager.make_connection(
                bind_user=self.user.dn,
                bind_password=self.user.userPassword,
                sasl_mechanism=EXTERNAL,
            )
            self._connection.open()

            if config['LDAP_USE_SSL']:
                self._connection.tls_started()
            self._connection.bind()

            self._connections[self.user.get_username_uid()] = self._connection

    def get_connection(self):
        return self._connection

    def show_connections(self):
        print('connection - ', self._connection.usage)
        for key, value in self._connections.items():
            print(value)
            print(f'key: {key}, value: , closed: {value.closed}, listening: {value.listening}')

    def rebind(self, user: User):
        self._connection.rebind(
            username=user.dn,
            password=user.userPassword,
        )

    def close_connection(self):
        """
        This function performs close connection
        :return: None
        """
        del self._connections[self.user.get_username_uid()]
        self._connection.unbind()


class UserManagerLDAP(ConnectionLDAP):

    def search(
        self,
        value,
        fields: Dict[str, str],
        attributes=ALL_ATTRIBUTES,
        required_fields: Dict[str, str] = None
    ) -> list:
        search_filter = '(|%s)' % "".join(
            [
                f'({field}={fields[field] % value})' for field in fields
                if (type(value) == int and fields[field] == '%d') or ('%s' in fields[field])
            ]
        )
        required_filter = '(&%s)' % "".join(
            [
                f'({key}={value_d})' for key, value_d in required_fields.items()
            ]
        )

        if required_fields and value:
            search_filter = '(&%s%s)' % (
                search_filter,
                required_filter
            )
        else:
            search_filter = required_filter

        status_search = self._connection.search(
            search_base='dc=example,dc=com',
            search_filter=search_filter,
            attributes=attributes
        )
        if not status_search:
            return []
        return self._connection.entries

    def get_user(self, uid, attributes=ALL_ATTRIBUTES) -> User:
        search = self.search(uid, {'uid': '%s'}, attributes=attributes)
        if not search:
            abort(404, 'User not found')

        data = orjson.loads(
            self._connection.entries[0].entry_to_json()
        )

        user = User(username_uid=uid, dn=data['dn'], **data['attributes'])
        return user

    def create_user(self, user: User, fields, operation) -> User:
        dn = user.dn

        self._connection.add(
            dn,
            attributes=user.serialize_data(
                fields=fields, operation=operation
            )
        )
        print('result: ', self._connection.result)
        return user

    def modify_user(self, user: User, fields, operation) -> User:
        founded_user = self.get_user(user.get_username_uid(), attributes=[])
        user.dn = founded_user.dn

        serialized_data_modify = user.serialize_data(
            fields=fields, operation=operation,
        )

        if founded_user:
            try:
                self._connection.modify(
                    user.dn,
                    {
                        key: [(
                            MODIFY_REPLACE,
                            value if type(value) == list else [value]
                        )]
                        for key, value in serialized_data_modify.items()
                    }
                )
                print('result:', self._connection.result)
            except LDAPInsufficientAccessRightsResult:
                abort(403, 'Insufficient access rights')
        return user

    def delete_user(self, user: User) -> bool:
        user = self.get_user(user.get_username_uid(), attributes=[])
        if not user:
            return False

        self._connection.delete(user.dn)
        print('DELETE user', self._connection.result)
        return True

    def get_users(self, *args, **kwargs) -> list:
        users = self.search(
            value=kwargs.get('value'),
            fields=kwargs.get('fields'),
            required_fields=kwargs.get('required_fields')
        )
        if not users:
            return []

        return [
            User(
                dn=user_json['dn'], **user_json['attributes']
            )
            for user in users if (user_json := orjson.loads(user.entry_to_json()))
        ]

    def get_groups(self, value, fields) -> list:
        search = self.search(value, fields)
        if not search:
            return []

        return [
            orjson.loads(group.entry_to_json()) for group in search
        ]

    def is_webadmin(self, dn) -> bool:
        groups = self.get_groups(Group.WEBADMINS.value, {'cn': '%s'})

        if not groups:
            return False

        member = groups[0]['attributes']['member']
        if dn not in member:
            return False

        return True


class AuthenticationLDAP(UserManagerLDAP):

    def authenticate(self):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username_uid(),
            password=self.user.userPassword
        )

        # if response.status.value == 2:
        #     users[self.user.get_username_uid()] = self.user.userPassword

        return response  # *.status: 2 - success, 1 - failed