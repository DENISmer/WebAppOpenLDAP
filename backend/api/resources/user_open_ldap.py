import pprint

from flask_restful import Resource, request, abort

from backend.api.common.auth_http_token import auth
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_user, define_schema
from backend.api.common.managers_ldap.group_ldap_manager import GroupManagerLDAP
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.paginator import Pagintion
from backend.api.common.user_manager import UserLdap, CnGroupLdap
from backend.api.config import settings
from backend.api.config.fields import (search_fields,
                                       webadmins_cn_posixgroup_fields)

from backend.api.common.roles import Role
from backend.api.resources import schema
from backend.api.resources.schema import UserOutSchemaToList


@auth.get_user_roles  # roles
def get_user_roles(user):
    return Role(user['role'])


class UserOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.serializer = CommonSerializer()

    def __modify_user_group(
        self,
        username_uid: str,
        user_fields,
        operation: str,
        deserialized_data
    ) -> UserLdap:

        user_obj = UserManagerLDAP(connection=self.connection)
        group_obj = GroupManagerLDAP(connection=self.connection)

        user = user_obj.item(
            username_uid
        )

        updated_user = UserLdap(
            dn=user.dn,
            username=username_uid,
            fields=user_fields['fields'],
            input_field_keys=deserialized_data.keys(),
            **deserialized_data,
        )

        if updated_user.uid is not None and username_uid not in updated_user.uid:
            updated_user.uid.append(username_uid)

        if updated_user.uidNumber:
            updated_user.gidNumber = updated_user.uidNumber
        if updated_user.gidNumber:
            updated_user.uidNumber = updated_user.gidNumber

        user_obj.modify(
            item=updated_user,
            operation=operation,
            not_modify_item=user
        )

        group = group_obj.get_group_info_posix_group(username_uid, abort_raise=False)

        if group and (updated_user.uidNumber or updated_user.gidNumber) \
                and group.gidNumber not in (updated_user.gidNumber, updated_user.uidNumber):
            group.gidNumber = updated_user.gidNumber or updated_user.uidNumber

            group_obj.modify(
                item=group,
                operation=operation,
            )  # must be test

        # update info user
        user.__dict__.update(deserialized_data)
        return user

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    @define_schema
    def get(self, username_uid, *args, **kwargs):
        user = UserManagerLDAP(connection=self.connection).item(username_uid)
        user_schema = kwargs['user_schema']

        serialized_user = self.serializer.serialize_data(user_schema, user)
        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    def put(self, username_uid, *args, **kwargs):
        json_data = request.get_json()
        user_schema = kwargs['user_schema']
        user_fields = kwargs['user_fields']

        deserialized_data = self.serializer.deserialize_data(user_schema, json_data, partial=False)
        print('deserialized_data', deserialized_data)
        user = self.__modify_user_group(
            username_uid=username_uid,
            deserialized_data=deserialized_data,
            user_fields=user_fields,
            operation='update'
        )

        serialized_user = self.serializer.serialize_data(user_schema, item=user)
        return serialized_user, 200

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    def patch(self, username_uid, *args, **kwargs):
        json_data = request.get_json()
        user_schema = kwargs['user_schema']
        user_fields = kwargs['user_fields']

        deserialized_data = self.serializer.deserialize_data(user_schema, json_data, partial=True)

        user = self.__modify_user_group(
            username_uid=username_uid,
            deserialized_data=deserialized_data,
            user_fields=user_fields,
            operation='update'
        )

        serialized_data = self.serializer.serialize_data(user_schema, user)
        return serialized_data, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_user()
    def delete(self, username_uid):
        user_obj = UserManagerLDAP(connection=self.connection)
        group_obj = GroupManagerLDAP(connection=self.connection)
        user = user_obj.item(username_uid, [])
        group = group_obj.get_group_info_posix_group(
            username_uid, [], abort_raise=False
        )

        user_obj.delete(item=user, operation='delete')
        if group:
            group_obj.delete(item=group, operation='delete')

        return None, 204


class UserListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.serializer = CommonSerializer()

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_user()
    def get(self, *args, **kwargs):
        user_schema = kwargs['user_schema']
        search = request.args.get('search', type=str)
        page = request.args.get('page', type=int, default=1)

        if search and len(search) < 2:
            return {
                'items': [],
                'num_pages': 1,
                'num_items': 0,
                'page': page,
            }, 200

        out_fields = getattr(schema, user_schema)().fetch_fields()
        users = UserManagerLDAP(connection=self.connection).list(
            value=search,
            fields=search_fields,
            attributes=out_fields,
            required_fields={'objectClass': 'person'},
        )

        items, num_users, num_pages = Pagintion(
            users, page, items_per_page=settings.ITEMS_PER_PAGE
        ).get_items()

        serialized_data = self.serializer.serialize_data(user_schema, items, many=True)

        return {
            'items': serialized_data,
            'num_pages': num_pages,
            'num_items': num_users,
            'page': page,
        }, 200

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_user()
    def post(self, *args, **kwargs):
        json_data = request.get_json()
        user_schema = kwargs['user_schema']
        user_fields = kwargs['user_fields']

        user_obj = UserManagerLDAP(connection=self.connection)
        group_obj = GroupManagerLDAP(connection=self.connection)

        deserialized_data = self.serializer.deserialize_data(user_schema, json_data, partial=False)

        if not deserialized_data.get('uidNumber') and not deserialized_data.get('gidNumber'):
            deserialized_data['uidNumber'] = \
                deserialized_data['gidNumber'] = user_obj.get_free_id_number()

        user = UserLdap(
            fields=user_fields['fields'],
            **deserialized_data
        )
        group = CnGroupLdap(
            cn=user.cn,
            memberUid=user.uid,
            objectClass=['posixGroup'],
            gidNumber=user.gidNumber,
            fields=webadmins_cn_posixgroup_fields['fields'],
        )
        group.dn = 'cn={0},{1}'.format(
            user.cn,
            str(group_obj.ldap_manager.full_group_search_dn)
        )

        found_user = user_obj.get_user_info_by_dn(user.dn, [])
        if found_user:
            abort(400, fields={'dn': 'The user already exists'}, status=400)

        #create objects
        user_obj.create(
            item=user,
            operation='create',
        )

        found_group = group_obj.get_group_info_posix_group(user.cn, [])
        if found_group:
            group_obj.create(
                item=group,
                operation='create',
            )

        if not deserialized_data.get('uidNumber') and not deserialized_data.get('gidNumber'):
            user_obj.free_id.del_from_reserved(user.gidNumber)

        serialized_users = self.serializer.serialize_data(user_schema, user)
        return serialized_users, 201


class UserMeOpenLDAPResource(Resource, CommonSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.serializer = CommonSerializer()

    @auth.login_required(role=[Role.WEBADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user(miss=True)
    def get(self, *args, **kwargs):
        current_user = auth.current_user()
        user_schema = kwargs['user_schema']

        user = UserManagerLDAP(connection=self.connection).item(current_user['uid'])
        serialized_data = self.serializer.serialize_data(user_schema, user)

        return serialized_data, 200
