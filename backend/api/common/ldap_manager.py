from __future__ import annotations

import pprint
import time
from typing import Dict

import orjson
import ssl

from flask_ldap3_login import LDAP3LoginManager
from flask_restful import abort

from ldap3 import Tls, ALL_ATTRIBUTES, Connection, MODIFY_REPLACE, EXTERNAL
from ldap3.core.exceptions import (LDAPInsufficientAccessRightsResult,
                                   LDAPAttributeError,
                                   LDAPException,
                                   LDAPEntryAlreadyExistsResult)

from backend.api.common.exceptions import ItemFieldsIsNone
from backend.api.common.groups import Group
from backend.api.common.user_manager import UserLdap, CnGroupLdap
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

    def __init__(self, user: UserLdap, *args, **kwargs):
        self.user = user
        self.ldap_manager = LDAPManager()
        self._connection = None

    def connect(self):
        """
        This function performs connection to OpenLDAP server
        :return: None
        """
        self._connection: Connection = self._connections.get(
            self.user.get_username()
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

            self._connections[self.user.get_username()] = self._connection

    def get_connection(self):
        return self._connection

    def show_connections(self):
        print('connection - ', self._connection.usage)
        for key, value in self._connections.items():
            print(value)
            print(f'key: {key}, value: , closed: {value.closed}, listening: {value.listening}')

    def rebind(self, user: UserLdap):
        self._connection.rebind(
            username=user.dn,
            password=user.userPassword,
        )

    def close_connection(self):
        """
        This function performs close connection
        :return: None
        """
        del self._connections[self.user.get_username()]
        self._connection.unbind()


class UserManagerLDAP(ConnectionLDAP):

    def search(
        self,
        value,
        fields: Dict[str, str],
        attributes=ALL_ATTRIBUTES,
        required_fields: Dict[str, str] = None
    ) -> list:

        search_filter = ''
        required_filter = ''

        if not value and not required_fields:
            return []

        if value:
            search_filter = '(|%s)' % "".join(
                [
                    f'({field}={fields[field] % value})' for field in fields
                    if (type(value) == int and fields[field] == '%d') or ('%s' in fields[field])
                ]
            )

        if required_fields:
            required_filter = '(|%s)' % "".join(
                [
                    f'({key}={value_d})' for key, value_d in required_fields.items()
                ]
            )

        common_filter = '(&%s%s)' % (
            search_filter,
            required_filter
        )

        status_search = self._connection.search(
            search_base=config['LDAP_BASE_DN'],
            search_filter=common_filter,
            attributes=attributes,
        )
        if not status_search:
            return []
        return self._connection.entries

    def get_user(self, uid, attributes=ALL_ATTRIBUTES) -> UserLdap:
        search = self.search(uid, {'uid': '%s'}, attributes=attributes)
        if not search:
            abort(404, message='User not found.')

        data = orjson.loads(
            self._connection.entries[0].entry_to_json()
        )
        pprint.pprint(data)
        user = UserLdap(username=uid, dn=data['dn'], **data['attributes'])
        return user

    def get_group_user(self, cn, attributes=ALL_ATTRIBUTES) -> CnGroupLdap:
        search = self.search(
            cn,
        {'cn': '%s', 'objectClass': 'posixGroup'},
            attributes=attributes
        )
        if not search:
            abort(404, message='User not found.')

        data = orjson.loads(
            self._connection.entries[0].entry_to_json()
        )
        pprint.pprint(data)
        group = CnGroupLdap(username=cn, dn=data['dn'], **data['attributes'])
        return group

    """
    CREATE USER
    
    "{
        "uidNumber": 1200, 
        "gidNumber": 1200, 
        "uid": "testuser", 
        "sshPublicKey": [], 
        "st": ['Moskow city'], 
        "mail": ["testuser@mail.ru", "testuser@mail.ru"], 
        "street": ['green street 12'], 
        "cn": ["Test User"], 
        "displayName": "Test User", 
        "givenName": ["testuser"], 
        "sn": ["Test User"], 
        "postalCode": [100123, 123414],
        "homeDirectory": "/home/testuser", 
        "loginShell": "/bin/bash", 
        "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"]
    }"
    
    """

    def create(self, item: UserLdap | CnGroupLdap, operation) -> UserLdap:

        if item.fields is None:
            raise ItemFieldsIsNone('Item fields is none.')

        try:
            self._connection.add(
                item.dn,
                attributes=item.serialize_data(
                    user_fields=item.fields,
                    operation=operation
                )
            )
        except LDAPInsufficientAccessRightsResult:
            abort(403, message='Insufficient access rights')

        except LDAPAttributeError as e:
            abort(400, message=str(e))

        except LDAPEntryAlreadyExistsResult as e:
            print(e)

        print('result create: ', self._connection.result)

        res = self._connection.result
        if 'success' not in res['description']:
            abort(400, message=res['message'])

        return item

    def modify(self,  item: UserLdap | CnGroupLdap, operation) -> UserLdap:

        serialized_data_modify = item.serialize_data(
            user_fields=item.fields,
            operation=operation,
        )

        try:
            self._connection.modify(
                item.dn,
                {
                    key: [(
                        MODIFY_REPLACE,
                        value if type(value) == list else [value]
                    )]
                    for key, value in serialized_data_modify.items()
                }
            )
            print('result modify:', self._connection.result)

            res = self._connection.result
            if 'success' not in res['description']:
                abort(400, message=res['message'])

        except LDAPInsufficientAccessRightsResult:
            abort(403, message='Insufficient access rights')
        except LDAPAttributeError as e:
            abort(400, message=str(e))

        return item

    def delete(self, user: UserLdap) -> bool:
        user = self.get_user(user.get_username(), attributes=[])
        if not user:
            return False

        self._connection.delete(user.dn)

        print('result delete:', self._connection.result)

        res = self._connection.result
        if 'success' in res['description']:
            abort(400, message=res['message'])

        return True

    def get_users(self, *args, **kwargs) -> list:
        try:
            users = self.search(
                value=kwargs.get('value'),
                fields=kwargs.get('fields'),
                attributes=kwargs.get('attributes'),
                required_fields=kwargs.get('required_fields')
            )
        except LDAPException as e:
            print('e:', e)
            abort(400, message=str(e))

        if not users:
            return []

        return [
            UserLdap(
                dn=user_json['dn'], **user_json['attributes']
            )
            for user in users if (user_json := orjson.loads(user.entry_to_json()))
        ]

    def get_groups(self, value, search_fields) -> list:
        search = self.search(value, search_fields)
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
            username=self.user.get_username(),
            password=self.user.userPassword,
        )

        # if response.status.value == 2:
        #     users[self.user.get_username_uid()] = self.user.userPassword

        return response  # *.status: 2 - success, 1 - failed