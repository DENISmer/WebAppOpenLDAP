from __future__ import annotations

from typing import Dict, List

from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ldap3.core.exceptions import (LDAPException,
                                   LDAPNoSuchObjectResult)
from flask_restful import abort

from backend.api.common.managers_ldap.common_ldap_manager import CommonManagerLDAP
from backend.api.common.getting_free_id import GetFreeId
from backend.api.common.user_manager import UserLdap, CnGroupLdap, GroupWebAdmins
from backend.api.config.fields import webadmins_cn_posixgroup_fields, search_fields


class UserManagerLDAP(CommonManagerLDAP):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.free_id = GetFreeId()

    def item(self, uid, attributes=ALL_ATTRIBUTES, abort_raise: bool = True) -> UserLdap | None:

        dn = 'uid={0},{1}'.format(
            uid,
            self.ldap_manager.full_user_search_dn
        )
        data = {}
        try:
            data = self.search_by_dn(dn=dn, filters='(objectClass=person)', attributes=attributes)
        except LDAPNoSuchObjectResult:
            if not abort_raise:
                return None
            abort(404, message='User not found.', status=404)

        return UserLdap(username=uid, dn=data['dn'], **data['attributes'])

    def list(self, *args, **kwargs) -> List[UserLdap]:

        users = self.search(
            value=kwargs.get('value'),
            fields=kwargs.get('fields'),
            attributes=kwargs.get('attributes'),
            required_fields=kwargs.get('required_fields')
        )

        if not users:
            return []

        return [
            UserLdap(
                dn=user['dn'], **user['attributes']
            )
            for user in users
        ]

    def is_webadmin(self, dn: str, groups: List[GroupWebAdmins]) -> bool:

        if not groups:
            return False
        member = groups[0].member or []
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

    def get_user_info_by_dn(self, dn: str, attributes=ALL_ATTRIBUTES):
        try:
            user = self.ldap_manager.get_object(
                dn=dn,
                filter='(objectClass=person)',
                attributes=attributes,
                _connection=self._connection,
            )
        except LDAPNoSuchObjectResult:
            return None
        return user
