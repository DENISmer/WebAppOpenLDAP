from __future__ import annotations

from typing import List

from flask_restful import abort
from ldap3 import ALL_ATTRIBUTES
from ldap3.core.exceptions import (LDAPException,
                                   LDAPNoSuchObjectResult)

from backend.api.common.groups import Group
from backend.api.common.managers_ldap.common_ldap_manager import CommonManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.user_manager import CnUserGroupLdap, GroupWebAdmins
from backend.api.config.fields import webadmins_cn_posixgroup_fields


class GroupManagerLDAP(CommonManagerLDAP):
    def list(self, *args, **kwargs) -> List[CnUserGroupLdap]:
        groups = self.search(
            value=kwargs.get('value'),
            fields=kwargs.get('fields'),
            attributes=kwargs.get('attributes'),
            required_fields=kwargs.get('required_fields')
        )
        if not groups:
            return []

        return [
            CnUserGroupLdap(dn=group['dn'], **group['attributes'])
            for group in groups
        ]

    def item(
        self,
        uid: str,
        type_group: list,
        fields: dict,
        attributes=ALL_ATTRIBUTES,
    ) -> CnUserGroupLdap | None:

        dn = 'cn={0},{1}'.format(
            uid,
            self.ldap_manager.full_group_search_dn
        )

        filter_group = '(&%s)' % (''.join(
            ['(objectClass=%s)' % group for group in type_group])
        )

        data = self.search_by_dn(dn=dn, filters=filter_group, attributes=attributes)
        if not data:
            return None

        group = CnUserGroupLdap(
            username=uid,
            dn=data['dn'],
            **data['attributes'],
            fields=fields['fields']
        )
        return group

    def get_webadmins_group(self) -> GroupWebAdmins:
        groups = self.search(
            value=Group.WEBADMINS.value,
            fields={'cn': '%s'},
            required_fields={'objectClass': 'groupOfNames'}
        )
        group = groups[0]
        member = list(map(lambda i: i.lower(), group['attributes']['member']))
        group['attributes']['member'] = member

        return GroupWebAdmins(
            dn=group['dn'], **group['attributes']
        )

    def get_group_info_posix_group(self, username_cn: str, attributes=ALL_ATTRIBUTES):
        return self.item(
            username_cn, ['posixGroup'],
            webadmins_cn_posixgroup_fields,
            attributes=attributes,
        )

    def is_webadmin(self, user) -> bool:
        group = self.get_webadmins_group()
        if not group:
            return False
        if user.dn not in group.member:
            return False

        return True
