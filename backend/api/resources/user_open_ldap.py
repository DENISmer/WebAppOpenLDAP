import logging
import os
import pprint
import time
import glob
import orjson

from flask_restful import Resource, request, abort

from backend.api.common.auth_http_token import auth
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_user, define_schema
from backend.api.common.managers_ldap.group_ldap_manager import GroupManagerLDAP
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.paginator import Pagintion
from backend.api.common.route import Route
from backend.api.common.user_manager import UserLdap, CnGroupLdap
from backend.api.common.validators import validate_uid_gid_number_to_unique
from backend.api.config import settings
from backend.api.config.fields import (search_fields,
                                       webadmins_cn_posixgroup_fields)

from backend.api.common.roles import Role
from backend.api.db.database import db
from backend.api.db.database_queries import DbQueries
from backend.api.db.models import TokenModel
from backend.api.resources import schema


@auth.get_user_roles  # roles
def get_user_roles(user):
    return Role(user['role'])


class UserOpenLDAPResource(Resource, CommonSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.route = Route.USERS

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
        if not user:
            abort(404, message='User not found', status=404)

        updated_user = UserLdap(
            dn=user.dn,
            username=username_uid,
            fields=user_fields['fields'],
            input_field_keys=deserialized_data.keys(),
            **deserialized_data,
        )

        if updated_user.uidNumber or updated_user.gidNumber:
            ids: list = user_obj.get_id_numbers()
            if user.uidNumber in ids:
                ids.remove(user.uidNumber)  # why?
            validate_uid_gid_number_to_unique(ids, updated_user.uidNumber, updated_user.gidNumber)

        if updated_user.uidNumber:
            deserialized_data['gidNumber'] = \
                updated_user.gidNumber = updated_user.uidNumber or user.uidNumber
        if updated_user.gidNumber:
            deserialized_data['uidNumber'] = \
                updated_user.uidNumber = updated_user.gidNumber or user.gidNumber

        user_obj.modify(
            item=updated_user,
            operation=operation,
            not_modify_item=user
        )

        group = group_obj.get_group_info_posix_group(username_uid)

        if group and (updated_user.uidNumber or updated_user.gidNumber) \
                and group.gidNumber not in (updated_user.gidNumber, updated_user.uidNumber):

            updated_user = CnGroupLdap(
                dn=group.dn,
                gidNumber=updated_user.gidNumber or updated_user.uidNumber,
                input_field_keys=['gidNumber'],
                fields=webadmins_cn_posixgroup_fields['fields'],
            )
            group_obj.modify(
                item=updated_user,
                operation=operation,
                not_modify_item=group
            )  # must be test

        elif not group:
            new_group = CnGroupLdap(
                cn=username_uid,
                memberUid=username_uid,
                objectClass=['posixGroup'],
                gidNumber=updated_user.gidNumber,
                fields=webadmins_cn_posixgroup_fields['fields'],
                input_field_keys=['cn', 'memberUid', 'objectClass', 'gidNumber']
            )
            new_group.dn = 'cn={0},{1}'.format(
                username_uid,
                str(group_obj.ldap_manager.full_group_search_dn)
            )
            group_obj.create(
                item=new_group,
                operation='create',
            )

        # update info user
        user.__dict__.update(deserialized_data)
        return user

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    @define_schema
    def get(self, username_uid, *args, **kwargs):
        user = UserManagerLDAP(connection=self.connection).item(username_uid)
        if not user:
            abort(404, message='User not found', status=404)

        user_schema = kwargs['schema']

        path = os.path.join(
            settings.ABSPATH_UPLOAD_FOLDER,
            f'{username_uid}*.*'
        )
        files = glob.glob(path)

        user.jpegPhotoPath = []
        for item in files:
            user.jpegPhotoPath.append(
                os.path.join(
                    '/', settings.UPLOAD_FOLDER, os.path.basename(item)
                )
            )

        serialized_user = self.serialize_data(user_schema, user)
        return serialized_user, 200

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    @define_schema
    def put(self, username_uid, *args, **kwargs):
        json_data = request.get_json()
        user_schema = kwargs['schema']
        user_fields = kwargs['fields']

        deserialized_data = self.deserialize_data(user_schema, json_data, partial=False)

        user = self.__modify_user_group(
            username_uid=username_uid,
            deserialized_data=deserialized_data,
            user_fields=user_fields,
            operation='update'
        )

        serialized_user = self.serialize_data(user_schema, item=user)
        return serialized_user, 200

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    @define_schema
    def patch(self, username_uid, *args, **kwargs):
        json_data = request.get_json()
        user_schema = kwargs['schema']
        user_fields = kwargs['fields']

        deserialized_data = self.deserialize_data(user_schema, json_data, partial=True)

        user = self.__modify_user_group(
            username_uid=username_uid,
            deserialized_data=deserialized_data,
            user_fields=user_fields,
            operation='update'
        )

        serialized_data = self.serialize_data(user_schema, user)
        return serialized_data, 200

    @auth.login_required(role=[Role.WEB_ADMIN])
    @connection_ldap
    @permission_user()
    def delete(self, username_uid):
        user_obj = UserManagerLDAP(connection=self.connection)
        group_obj = GroupManagerLDAP(connection=self.connection)
        user = user_obj.item(username_uid, [])

        if not user:
            abort(404, message='User not found', status=404)

        group = group_obj.get_group_info_posix_group(
            username_uid, []
        )

        db_queries = DbQueries(db.session)
        db_queries.delete_instance_by_params(TokenModel, dn=user.dn)

        user_obj.delete(item=user, operation='delete')
        if group:
            group_obj.delete(item=group, operation='delete')

        return None, 204


class UserListOpenLDAPResource(Resource, CommonSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.route = Route.USERS

    @auth.login_required(role=[Role.WEB_ADMIN])
    @connection_ldap
    @permission_user()
    @define_schema
    def get(self, *args, **kwargs):
        user_schema = kwargs['schema']
        search = request.args.get('search', type=str)
        page = request.args.get('page', type=int, default=1) or 1

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

        serialized_data = self.serialize_data(user_schema, items, many=True)

        return {
            'items': serialized_data,
            'num_pages': num_pages,
            'num_items': num_users,
            'page': page,
        }, 200

    @auth.login_required(role=[Role.WEB_ADMIN])
    @connection_ldap
    @permission_user()
    @define_schema
    def post(self, *args, **kwargs):
        json_data = request.get_json()
        user_schema = kwargs['schema']
        user_fields = kwargs['fields']

        user_obj = UserManagerLDAP(connection=self.connection)
        group_obj = GroupManagerLDAP(connection=self.connection)

        deserialized_data = self.deserialize_data(user_schema, json_data, partial=False)

        uid_number, gid_number = deserialized_data.get('uidNumber'), deserialized_data.get('gidNumber')
        if uid_number or gid_number:
            ids = user_obj.get_id_numbers()
            validate_uid_gid_number_to_unique(ids, uid_number, gid_number)
        elif not uid_number and not gid_number:
            deserialized_data['uidNumber'] = \
                deserialized_data['gidNumber'] = user_obj.get_free_id_number()

        user = UserLdap(
            fields=user_fields['fields'],
            input_field_keys=deserialized_data.keys(),
            **deserialized_data
        )
        group = CnGroupLdap(
            cn=user.uid,
            memberUid=user.uid,
            objectClass=['posixGroup'],
            gidNumber=user.gidNumber,
            fields=webadmins_cn_posixgroup_fields['fields'],
            input_field_keys=['cn', 'memberUid', 'objectClass', 'gidNumber']
        )
        group.dn = 'cn={0},{1}'.format(
            user.uid,
            str(group_obj.ldap_manager.full_group_search_dn)
        )

        #create objects
        user_obj.create(
            item=user,
            operation='create',
        )

        found_group = group_obj.get_group_info_posix_group(user.uid, [])
        if found_group:
            group_obj.delete(found_group)

        group_obj.create(
            item=group,
            operation='create',
        )

        user_obj.free_id.delete_from_reserved(user.gidNumber)

        serialized_users = self.serialize_data(user_schema, user)
        return serialized_users, 201


class UserMeOpenLDAPResource(Resource, CommonSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.route = Route.USERS

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user(miss=True)
    @define_schema
    def get(self, *args, **kwargs):
        current_user = auth.current_user()
        user_schema = kwargs['schema']

        user = UserManagerLDAP(connection=self.connection).item(current_user['uid'])
        serialized_data = self.serialize_data(user_schema, user)

        return serialized_data, 200
