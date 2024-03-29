from __future__ import annotations

from typing import Dict, List

from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ldap3.core.exceptions import (LDAPException,
                                   LDAPNoSuchObjectResult)
from flask_restful import abort

from backend.api.common.managers_ldap.common_ldap_manager import CommonManagerLDAP
from backend.api.common.getting_free_id import GetFreeId
from backend.api.common.user_manager import UserLdap, CnUserGroupLdap, GroupWebAdmins


class UserManagerLDAP(CommonManagerLDAP):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('free_id_use'):
            self.free_id = GetFreeId()

    def item(self, uid, attributes=ALL_ATTRIBUTES) -> UserLdap | None:

        dn = 'uid={0},{1}'.format(
            uid,
            self.ldap_manager.full_user_search_dn
        )

        data = self.search_by_dn(dn=dn, filters='(objectClass=person)', attributes=attributes)
        if not data:
            return None

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

    def get_free_id_number(self):
        unique_ids = self.get_id_numbers()
        return self.free_id.get_free_spaces(unique_ids)

    def get_user_info_by_dn(self, dn: str, attributes=ALL_ATTRIBUTES):
        user = self.search_by_dn(
            dn=dn, filters='(objectClass=person)', attributes=attributes
        )
        return user
