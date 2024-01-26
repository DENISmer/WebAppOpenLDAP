from __future__ import annotations

import logging
import pprint
from typing import Dict
import orjson

from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ldap3.core.exceptions import (LDAPInsufficientAccessRightsResult,
                                   LDAPAttributeError,
                                   LDAPException,
                                   LDAPEntryAlreadyExistsResult,
                                   LDAPInvalidDnError,
                                   LDAPInvalidDNSyntaxResult,
                                   LDAPObjectClassError, LDAPNoSuchObjectResult, LDAPOperationResult)
from flask_restful import abort

from backend.api.common.connection_ldap import ConnectionLDAP
from backend.api.common.decorators import error_operation_ldap
from backend.api.common.exceptions import ItemFieldsIsNone, get_attribute_error_fields
from backend.api.common.getting_free_id import GetFreeId
from backend.api.common.groups import Group
from backend.api.common.user_manager import UserLdap, CnGroupLdap
from backend.api.config.fields import webadmins_cn_group_fields, search_fields
from backend.api.config.ldap import config


class UserManagerLDAP(ConnectionLDAP, GetFreeId):

    def search(
        self,
        value,
        fields: Dict[str, str],
        attributes=ALL_ATTRIBUTES,
        required_fields: Dict[str, str] = None,
    ) -> list:

        search_filter = ''
        required_filter = ''

        if not value and not required_fields:
            return []

        if value:
            search_filter = '(|%s)' % "".join(
                [
                    f'({field}={fields[field] % value})' for field in fields
                    if (type(value) == int and fields[field] == '%d')
                       or ('%s' in fields[field])
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

    def get_user(self, uid, attributes=ALL_ATTRIBUTES, abort_raise=True) -> UserLdap | None:

        dn = 'uid={0},{1}'.format(
            uid,
            self.ldap_manager.full_user_search_dn
        )
        data = {}
        try:
            data = self.ldap_manager.get_object(
                dn=dn,
                filter='(objectClass=person)',
                attributes=attributes,
                _connection=None,
            )
        except LDAPNoSuchObjectResult:
            if not abort_raise:
                return None
            abort(404, message='User not found.')

        return UserLdap(username=uid, **data)

    def get_group_info_posix_group(self, uid, attributes=ALL_ATTRIBUTES, abort_raise=True) -> CnGroupLdap | None:

        dn = 'cn={0},{1}'.format(
            uid,
            self.ldap_manager.full_group_search_dn
        )
        data = {}
        try:
            data = self.ldap_manager.get_object(
                dn=dn,
                filter='(objectClass=posixGroup)',
                attributes=attributes,
                _connection=None,
            )
        except LDAPNoSuchObjectResult:
            if not abort_raise:
                return None
            abort(404, message='Group not found.')

        group = CnGroupLdap(
            username=uid,
            **data,
            fields=webadmins_cn_group_fields['fields']
        )
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

    @error_operation_ldap
    def create(self, item: UserLdap | CnGroupLdap, operation) -> UserLdap:

        if item.fields is None:
            raise ItemFieldsIsNone('Item fields is none.')

        self._connection.add(
            item.dn,
            attributes=item.serialize_data(
                user_fields=item.fields,
                operation=operation
            )
        )

        res = self._connection.result

        # abort(400, message=res['message'])
        if 'success' not in res['description']:
            abort(400, message=res['message'])
        print('Success')

        return item

    @error_operation_ldap
    def modify(self,  item: UserLdap | CnGroupLdap, operation) -> UserLdap | CnGroupLdap:

        serialized_data_modify = item.serialize_data(
            user_fields=item.fields,
            operation=operation,
        )

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
            abort(400, message=res['description'])

        return item

    @error_operation_ldap
    def delete(self, item: UserLdap | CnGroupLdap, operation='delete'):
        if item.dn:
            self._connection.delete(item.dn)

        print('result delete:', self._connection.result)

        res = self._connection.result
        if 'success' not in res['description']:
            abort(400, message=f'Error deletion {item.dn}')

    def get_users(self, *args, **kwargs) -> list:
        users = []
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

    def get_posix_group(self, value, search_fields, required_fields):
        pass

    def get_groups(self, value, search_fields, required_fields) -> list:
        groups = self.search(value, fields=search_fields, required_fields=required_fields)
        if not groups:
            return []

        return [
            {
                'dn': json_data['dn'],
                **json_data['attributes']
            }
            for group in groups if (json_data := orjson.loads(group.entry_to_json()))
        ]

    def is_webadmin(self, dn) -> bool:
        groups = self.get_groups(
            Group.WEBADMINS.value,
            {'cn': '%s'},
            {'objectClass': 'groupOfNames'}
        )
        if not groups:
            return False
        member = groups[0]['member']
        if dn not in member:
            return False

        return True

    def get_free_id_number(self):
        users = self.get_users(
            value=None,
            fields=search_fields,
            attributes=['uidNumber'],
            required_fields={'objectClass': 'person'},
        )

        ids = []
        for user in users:
            ids.append(user.uidNumber)

        unique_ids = set(ids)
        return self.get_free_spaces(unique_ids)
