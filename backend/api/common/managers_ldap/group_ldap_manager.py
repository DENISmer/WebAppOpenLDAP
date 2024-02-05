from __future__ import annotations

from flask_restful import abort
from ldap3 import ALL_ATTRIBUTES
from ldap3.core.exceptions import (LDAPException,
                                   LDAPNoSuchObjectResult)

from backend.api.common.groups import Group
from backend.api.common.managers_ldap.common_ldap_manager import CommonManagerLDAP
from backend.api.common.user_manager import CnGroupLdap
from backend.api.config.fields import webadmins_cn_posixgroup_fields


class GroupManagerLDAP(CommonManagerLDAP):
    def list(self, *args, **kwargs) -> list:
        groups = self.search(
            value=kwargs.get('value'),
            fields=kwargs.get('fields'),
            attributes=kwargs.get('attributes'),
            required_fields=kwargs.get('required_fields')
        )
        if not groups:
            return []

        return [
            CnGroupLdap(dn=group['dn'], **group['attributes'])
            for group in groups
        ]

    def item(
        self,
        uid: str,
        type_group: list,
        fields: dict,
        attributes=ALL_ATTRIBUTES,
        abort_raise=True
    ) -> CnGroupLdap | None:

        dn = 'cn={0},{1}'.format(
            uid,
            self.ldap_manager.full_group_search_dn
        )
        data = {}
        filter_group = '(&%s)' % (''.join(
            ['(objectClass=%s)' % group for group in type_group])
        )
        try:
            data = self.ldap_manager.get_object(
                dn=dn,
                filter=filter_group, #'(objectClass=posixGroup)',
                attributes=attributes,
                _connection=self._connection,
            )
        except LDAPNoSuchObjectResult:
            if not abort_raise:
                return None
            abort(404, message='Group not found.')

        group = CnGroupLdap(
            username=uid,
            **data,
            fields=fields['fields']
        )
        return group

    def get_webadmins_groups(self) -> list:
        groups = self.search(
            value=Group.WEBADMINS.value,
            fields={'cn': '%s'},
            required_fields={'objectClass': 'groupOfNames'}
        )

        return [
            CnGroupLdap(dn=group['dn'], **group['attributes'])
            for group in groups
        ]

    def get_group_info_posix_group(self, username_cn: str, attributes=ALL_ATTRIBUTES, abort_raise: bool = True):
        return self.item(
            username_cn, ['posixGroup'],
            webadmins_cn_posixgroup_fields,
            attributes=attributes,
            abort_raise=abort_raise
        )


