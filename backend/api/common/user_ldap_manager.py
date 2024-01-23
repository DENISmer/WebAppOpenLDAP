from __future__ import annotations

import pprint
from typing import Dict
import orjson

from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ldap3.core.exceptions import (LDAPInsufficientAccessRightsResult,
                                   LDAPAttributeError,
                                   LDAPException,
                                   LDAPEntryAlreadyExistsResult)
from flask_restful import abort

from backend.api.common.connection_ldap import ConnectionLDAP
from backend.api.common.exceptions import ItemFieldsIsNone
from backend.api.common.groups import Group
from backend.api.common.user_manager import UserLdap, CnGroupLdap
from backend.api.config.fields import cn_group_fields
from backend.api.config.ldap import config


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

    def get_group_info_posix_group(self, uid, attributes=ALL_ATTRIBUTES) -> CnGroupLdap:
        search = self.search(
            uid,
            {'cn': '%s', 'objectClass': 'posixGroup'},
            attributes=attributes
        )
        if not search:
            abort(404, message='Group not found.')
        print(self._connection.entries[0])
        data = orjson.loads(
            self._connection.entries[0].entry_to_json()
        )

        group = CnGroupLdap(username=uid, dn=data['dn'], **data['attributes'], fields=cn_group_fields['fields'])
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
        if 'success' not in res['description']:
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