from __future__ import annotations

import pprint

from flask_restful import Resource, request

from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_group
from backend.api.common.auth_http_token import auth
from backend.api.common.roles import Role
from backend.api.common.user_ldap_manager import UserManagerLDAP
from backend.api.common.user_manager import CnGroupLdap
from backend.api.resources import schema


class GroupOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_manager_ldap: UserManagerLDAP = None
        self.serializer = CommonSerializer()

    def __modify_group(
        self,
        username_cn,
        deserialized_data,
        group_fields,
        webadmins_user_fields,
        update_gid_number_user: bool = False
    ) -> CnGroupLdap | None:

        group = self._user_manager_ldap.get_group_info_posix_group(username_cn, [])
        updated_group = CnGroupLdap(
            username=username_cn,
            dn=group.dn,
            **deserialized_data,
            fields=group_fields['fields']
        )

        if username_cn not in updated_group.cn:
            updated_group.cn.append(username_cn)

        if updated_group.gidNumber and group.gidNumber != updated_group.gidNumber and update_gid_number_user:
            user = self._user_manager_ldap.get_user(username_cn, [], abort_raise=False)
            user.fields = webadmins_user_fields['fields']
            user.gidNumber = user.uidNumber = updated_group.gidNumber
            self._user_manager_ldap.modify(user, 'update')

        updated_group = self._user_manager_ldap.modify(updated_group, 'update')
        return updated_group

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def get(self, username_cn, type_group, *args, **kwargs):
        group_schema = kwargs['group_schema']
        group = self._user_manager_ldap.get_group_info_posix_group(username_cn)
        serialized_data = self.serializer.serialize_data(group_schema, group, many=False)
        return serialized_data, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def put(self, username_cn, type_group, *args, **kwargs):
        group_schema = kwargs['group_schema']
        group_fields = kwargs['group_fields']
        webadmins_user_fields = kwargs['webadmins_user_fields']
        json_data = request.get_json()

        deserialized_data = self.serializer.deserialize_data(group_schema, json_data, partial=False)
        updated_group = self.__modify_group(
            username_cn, deserialized_data, group_fields, webadmins_user_fields, True
        )
        serialized_user = self.serializer.serialize_data(group_schema, item=updated_group)

        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def patch(self, username_cn, type_group, *args, **kwargs):
        group_schema = kwargs['group_schema']
        group_fields = kwargs['group_fields']
        webadmins_user_fields = kwargs['webadmins_user_fields']
        json_data = request.get_json()

        deserialized_data = self.serializer.deserialize_data(group_schema, json_data, partial=True)
        updated_group = self.__modify_group(
            username_cn, deserialized_data,
            group_fields, webadmins_user_fields,
            True
        )
        serialized_user = self.serializer.serialize_data(group_schema, item=updated_group)

        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def delete(self, username_cn, type_group, *args, **kwargs):
        group = self._user_manager_ldap.get_group_info_posix_group(username_cn, [])
        self._user_manager_ldap.delete(group)
        return None, 204


class GroupListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_manager_ldap: UserManagerLDAP = None
        self.serializer = CommonSerializer()

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def get(self, type_group, *args, **kwargs):
        group_schema = kwargs['group_schema']
        out_fields = getattr(schema, group_schema)().fetch_fields()
        json_groups = self._user_manager_ldap.get_groups(
            value=None,
            fields=None,
            required_fields={'objectClass':  type_group},
            attributes=out_fields
        )
        groups = [
            CnGroupLdap(**group) for group in json_groups
        ]
        serialized_data = self.serializer.serialize_data(group_schema, groups, many=True)
        return {"groups": serialized_data}, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def post(self, *args, **kwargs):
        json_data = request.get_json()
        group_schema = kwargs['group_schema']
        group_field = kwargs['group_fields']
        deserialized_data = self.serializer.deserialize_data(group_schema, json_data)

        group = CnGroupLdap(
            **deserialized_data,
            fields=group_field['fields']
        )
        new_group = self._user_manager_ldap.create(group, 'create')

        serialized_data = self.serializer.serialize_data(group_schema, new_group, many=False)
        return serialized_data, 201
