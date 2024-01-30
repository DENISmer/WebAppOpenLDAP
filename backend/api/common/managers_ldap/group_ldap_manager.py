import orjson

from flask_restful import abort
from ldap3 import ALL_ATTRIBUTES
from ldap3.core.exceptions import (LDAPException,
                                   LDAPNoSuchObjectResult)

from backend.api.common.managers_ldap.common_ldap_manager import CommonManagerLDAP
from backend.api.common.user_manager import CnGroupLdap


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
            {
                'dn': json_data['dn'],
                **json_data['attributes']
            }
            for group in groups if (json_data := orjson.loads(group.entry_to_json()))
        ]

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