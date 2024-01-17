import pprint
import time
from typing import List, Dict

import orjson
import ssl

from flask_ldap3_login import LDAP3LoginManager
from flask import abort

from ldap3 import Tls, ALL_ATTRIBUTES, Connection, MODIFY_REPLACE, EXTERNAL
from ldap3.core.exceptions import LDAPInsufficientAccessRightsResult

from backend.api.common.user_manager import User
from backend.api.config.fields import search_fields, admin_fields
from backend.api.config.ldap import config


users = {

}


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
            self.tls_ctx = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1,
                               ca_certs_file=config['CERT_PATH'])


class InitLdap:
    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        self.ldap_manager = LDAPManager()


class AuthenticationLDAP(InitLdap):

    def authenticate(self):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username_uid(),
            password=self.user.userPassword
        )

        if response.status.value == 2:
            print('STATUS: SUCCESS, user uid:', self.user.get_username_uid())
            users[self.user.get_username_uid()] = self.user.userPassword

            pprint.pprint(users)

        return response  # *.status: 2 - success, 1 - failed


class ConnectionLDAP(InitLdap):
    _connections = {}

    def __init__(
        self,
        user: User,
        *args,
        **kwargs
    ):

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

    def rebind(self, user: User):
        self._connection.rebind(
            username=user.dn,
            password=user.userPassword,
        )

    def get_connection(self):
        return self._connection

    def close(self):
        """
        This function performs close connection
        :return: None
        """
        del self._connections[self.user.get_username_uid()]
        self._connection.unbind()

    def search(
        self,
        value,
        fields: Dict[str, str],
        attributes=ALL_ATTRIBUTES
    ):

        status_search = self._connection.search(
            search_base='dc=example,dc=com',
            search_filter='(|%s)' % "".join(
                [f'({field}={fields[field] % value})' for field in fields]
            ),
            attributes=attributes
        )
        if not status_search:
            return []
        return self._connection.entries

    def get_user(
        self,
        uid,
        attributes=ALL_ATTRIBUTES
    ) -> User:
        search = self.search(uid, {'uid': '%s'}, attributes=attributes)
        if not search:
            abort(404, 'User not found')

        data = orjson.loads(
            self._connection.entries[0].entry_to_json()
        )

        user = User(username_uid=uid, dn=data['dn'], **data['attributes'])
        return user

    def create_user(self, user: User, fields, operation):
        dn = user.dn

        self._connection.add(
            dn,
            attributes=user.serialize_data(
                fields=fields, operation=operation
            )
        )
        print('result: ', self._connection.result)

    def modify_user(self, user: User, fields, operation):
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
                        key: [(MODIFY_REPLACE, value if type(value) == list else [value])]
                        for key, value in serialized_data_modify.items()
                    }
                )
                print('result:', self._connection.result)
            except LDAPInsufficientAccessRightsResult:
                abort(403, 'Insufficient access rights')
        return user

    def delete_user(self, user: User):
        user = self.get_user(user.get_username_uid(), attributes=[])
        if not user:
            return False

        self._connection.delete(user.dn)
        return True

    def get_users(self):
        pass

    def get_groups(self):
        pass

    def is_webadmin(self):
        print('webadmin:', self.search('webadmins', {'cn': '*%s*'}))
