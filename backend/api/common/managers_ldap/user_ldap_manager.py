from __future__ import annotations

from typing import Dict, List
import orjson

from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ldap3.core.exceptions import (LDAPException,
                                   LDAPNoSuchObjectResult)
from flask_restful import abort

from backend.api.common.managers_ldap.common_ldap_manager import CommonManagerLDAP
from backend.api.common.managers_ldap.connection_ldap_manager import ConnectionManagerLDAP
from backend.api.common.decorators import error_operation_ldap
from backend.api.common.exceptions import ItemFieldsIsNone
from backend.api.common.getting_free_id import GetFreeId
from backend.api.common.groups import Group
from backend.api.common.user_manager import UserLdap, CnGroupLdap
from backend.api.config.fields import webadmins_cn_posixgroup_fields, search_fields
from backend.api.config.ldap import config


class UserManagerLDAP(CommonManagerLDAP):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.free_id = GetFreeId()

    def item(self, uid, attributes=ALL_ATTRIBUTES, abort_raise=True) -> UserLdap | None:

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
            abort(404, message='User not found.', status=404)

        return UserLdap(username=uid, **data)

    def list(self, *args, **kwargs) -> List[UserLdap]:
        users = []
        # try:
        users = self.search(
            value=kwargs.get('value'),
            fields=kwargs.get('fields'),
            attributes=kwargs.get('attributes'),
            required_fields=kwargs.get('required_fields')
        )
        # except LDAPException as e:
        #     print('e:', e)
        #     abort(400, message=str(e), status=400)

        if not users:
            return []

        return [
            UserLdap(
                dn=user_json['dn'], **user_json['attributes']
            )
            for user in users if (user_json := orjson.loads(user.entry_to_json()))
        ]

    def is_webadmin(self, dn, groups) -> bool:

        if not groups:
            return False
        member = groups[0]['attributes']['member']
        if dn not in member:
            return False

        return True

    def get_free_id_number(self):
        users = self.list(
            value=None,
            fields=search_fields,
            attributes=['uidNumber'],
            required_fields={'objectClass': 'person'},
        )

        ids = []
        for user in users:
            ids.append(user.uidNumber)

        unique_ids = set(ids)
        return self.free_id.get_free_spaces(unique_ids)
