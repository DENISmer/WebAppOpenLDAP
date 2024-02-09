from __future__ import annotations

import pprint

from flask_restful import Resource, request

from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_group, define_schema
from backend.api.common.auth_http_token import auth
from backend.api.common.managers_ldap.group_ldap_manager import GroupManagerLDAP
from backend.api.common.paginator import Pagintion
from backend.api.common.roles import Role
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.user_manager import CnGroupLdap
from backend.api.config import settings
from backend.api.config.fields import webadmins_cn_posixgroup_fields, search_posixgroup_fields
from backend.api.resources import schema
from backend.api.resources.schema import CnGroupOutSchemaToList


class GroupOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.serializer = CommonSerializer()

    def __modify_group(
        self,
        username_cn,
        deserialized_data,
        group_fields,
        user_fields,
        update_gid_number_user: bool = False
    ) -> CnGroupLdap | None:
        group_obj = GroupManagerLDAP(connection=self.connection)
        user_obj = UserManagerLDAP(connection=self.connection)

        group = group_obj.get_group_info_posix_group(username_cn)

        updated_group = CnGroupLdap(
            username=username_cn,
            dn=group.dn,
            **deserialized_data,
            fields=group_fields['fields']
        )

        if updated_group.gidNumber and group.gidNumber != updated_group.gidNumber and update_gid_number_user:
            user = user_obj.item(username_cn, [], abort_raise=False)
            user.fields = user_fields['fields']
            user.gidNumber = user.uidNumber = updated_group.gidNumber
            user_obj.modify(item=user, operation='update')

        updated_group = group_obj.modify(item=updated_group, operation='update')
        group.__dict__.update(deserialized_data)
        return group

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def get(self, username_cn, type_group, *args, **kwargs):
        group_schema = kwargs['group_schema']
        group = GroupManagerLDAP(connection=self.connection) \
            .get_group_info_posix_group(username_cn)
        serialized_data = self.serializer.serialize_data(group_schema, group, many=False)
        return serialized_data, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def put(self, username_cn, type_group, *args, **kwargs):
        group_schema = kwargs['schema']
        group_fields = kwargs['fields']
        webadmins_user_fields = kwargs['webadmins_fields']
        json_data = request.get_json()

        deserialized_data = self.serializer.deserialize_data(group_schema, json_data, partial=False)
        updated_group = self.__modify_group(
            username_cn, deserialized_data, group_fields,
            webadmins_user_fields, True
        )
        serialized_user = self.serializer.serialize_data(group_schema, item=updated_group)

        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def patch(self, username_cn, type_group, *args, **kwargs):
        group_schema = kwargs['schema']
        group_fields = kwargs['fields']
        webadmins_user_fields = kwargs['webadmins_fields']
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
    @define_schema
    def delete(self, username_cn, type_group, *args, **kwargs):
        group_obj = GroupManagerLDAP(connection=self.connection)
        group = group_obj.get_group_info_posix_group(username_cn)
        group_obj.delete(item=group, operation='delete')
        return None, 204


class GroupListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.serializer = CommonSerializer()

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def get(self, type_group, *args, **kwargs):
        group_schema = kwargs['schema']
        search = request.args.get('search', type=str)
        page = request.args.get('page', type=int, default=1) or 1

        out_fields = getattr(schema, group_schema)().fetch_fields()
        groups = GroupManagerLDAP(connection=self.connection).list(
            value=search,
            fields=search_posixgroup_fields,
            required_fields={'objectClass':  type_group},
            attributes=out_fields
        )

        items, num_items, num_pages = Pagintion(
            groups, page, items_per_page=settings.ITEMS_PER_PAGE
        ).get_items()

        serialized_data = self.serializer.serialize_data(group_schema, items, many=True)

        return {
            'items': serialized_data,
            'num_pages': num_pages,
            'num_items': num_items,
            'page': page,
        }, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def post(self, *args, **kwargs):
        json_data = request.get_json()
        group_schema = kwargs['schema']
        group_field = kwargs['fields']
        deserialized_data = self.serializer.deserialize_data(group_schema, json_data)

        group = CnGroupLdap(
            **deserialized_data,
            fields=group_field['fields']
        )
        new_group = GroupManagerLDAP(connection=self.connection).create(item=group, operation='create')

        serialized_data = self.serializer.serialize_data(group_schema, new_group, many=False)
        return serialized_data, 201
