from __future__ import annotations

from flask_restful import Resource, request, abort

from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_group, define_schema
from backend.api.common.auth_http_token import auth
from backend.api.common.groups import Group
from backend.api.common.managers_ldap.group_ldap_manager import GroupManagerLDAP
from backend.api.common.paginator import Pagintion
from backend.api.common.roles import Role
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.user_manager import CnGroupLdap, UserLdap
from backend.api.common.validators import validate_uid_gid_number_to_unique
from backend.api.config import settings
from backend.api.config.fields import search_posixgroup_fields
from backend.api.resources import schema


class GroupOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.serializer = CommonSerializer()

    def __modify_group(
        self,
        username_uid,
        deserialized_data,
        group_fields,
        user_fields,
        update_gid_number_user: bool = False
    ) -> CnGroupLdap | None:
        group_obj = GroupManagerLDAP(connection=self.connection)
        user_obj = UserManagerLDAP(connection=self.connection)

        group = group_obj.get_group_info_posix_group(username_uid)
        if not group:
            abort(404, message='Group not found', status=404)

        updated_group = CnGroupLdap(
            username=username_uid,
            dn=group.dn,
            input_field_keys=deserialized_data.keys(),
            **deserialized_data,
            fields=group_fields['fields']
        )

        if updated_group.gidNumber and group.gidNumber != updated_group.gidNumber and update_gid_number_user:
            user = user_obj.item(username_uid)
            if user:
                updated_users = UserLdap(
                    dn=user.dn,
                    fields=user_fields['fields'],
                    input_field_keys=['gidNumber', 'uidNumber'],
                    gidNumber=updated_group.gidNumber,
                    uidNumber=updated_group.gidNumber,
                )
                user_obj.modify(item=updated_users, operation='update', not_modify_item=user)

        group_obj.modify(item=updated_group, operation='update', not_modify_item=group)
        group.__dict__.update(deserialized_data)
        return group

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def get(self, group_username_uid, type_group, *args, **kwargs):
        username_uid = group_username_uid
        group = GroupManagerLDAP(connection=self.connection) \
            .get_group_info_posix_group(username_uid)
        if not group:
            abort(404, message='Group not found', status=404)

        group_schema = kwargs['schema']
        serialized_data = self.serializer.serialize_data(group_schema, group, many=False)
        return serialized_data, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def put(self, group_username_uid, type_group, *args, **kwargs):
        username_uid = group_username_uid
        group_schema = kwargs['schema']
        group_fields = kwargs['fields']
        webadmins_user_fields = kwargs['webadmins_fields']
        json_data = request.get_json()

        deserialized_data = self.serializer.deserialize_data(group_schema, json_data, partial=False)
        updated_group = self.__modify_group(
            username_uid, deserialized_data, group_fields,
            webadmins_user_fields, True
        )
        serialized_user = self.serializer.serialize_data(group_schema, item=updated_group)

        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    @define_schema
    def patch(self, group_username_uid, type_group, *args, **kwargs):
        username_uid = group_username_uid
        group_schema = kwargs['schema']
        group_fields = kwargs['fields']
        webadmins_user_fields = kwargs['webadmins_fields']
        json_data = request.get_json()

        deserialized_data = self.serializer.deserialize_data(group_schema, json_data, partial=True)
        updated_group = self.__modify_group(
            username_uid, deserialized_data,
            group_fields, webadmins_user_fields,
            True
        )
        serialized_user = self.serializer.serialize_data(group_schema, item=updated_group)

        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_group
    def delete(self, group_username_uid, type_group, *args, **kwargs):
        username_uid = group_username_uid
        group_obj = GroupManagerLDAP(connection=self.connection)
        group = group_obj.get_group_info_posix_group(username_uid)

        if not group:
            abort(404, message='Group not found', status=404)

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
        group_obj = GroupManagerLDAP(connection=self.connection)
        deserialized_data = self.serializer.deserialize_data(group_schema, json_data)

        group = CnGroupLdap(
            **deserialized_data,
            fields=group_field['fields'],
            input_field_keys=deserialized_data.keys(),
        )

        found_group_ids = group_obj.get_id_numbers(
            required_fields={'objectClass': Group.POSIXGROUP.value}
        )
        validate_uid_gid_number_to_unique(found_group_ids, gid_number=group.gidNumber)

        new_group = group_obj.create(item=group, operation='create')

        serialized_data = self.serializer.serialize_data(group_schema, new_group, many=False)
        return serialized_data, 201
