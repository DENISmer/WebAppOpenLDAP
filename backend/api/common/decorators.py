import functools

from flask_restful import abort

from backend.api.common.auth_http_token import auth
from backend.api.common.ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.user_manager import User
from backend.api.config.fields import simple_user_fields, webadmins_fields
from backend.api.resources.schema import SimpleUserSchemaLdapModify, WebAdminsSchemaLdapModify, \
    WebAdminsSchemaLdapCreate, WebAdminsSchemaLdapList


def connection_ldap(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        # args[0] - self of the function
        user_manager_ldap = getattr(args[0], '_user_manager_ldap')
        if hasattr(args[0], '_user_manager_ldap') or not user_manager_ldap:
            current_user = auth.current_user()
            user_manager_ldap = UserManagerLDAP(
                User(
                    dn='uid=bob,ou=People,dc=example,dc=com',
                    username_uid='bob',
                    userPassword='bob',
                )
            )
            setattr(args[0], '_user_manager_ldap', user_manager_ldap)
        user_manager_ldap.connect()

        res = func(*args, **kwargs)
        return res

    return wraps


def permission_user(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        current_user = auth.current_user()
        username_uid = kwargs.get('username_uid')

        if current_user['uid'] != username_uid and not current_user['role'] == Role.WEBADMIN.value:
            abort(403, message='Insufficient access rights.')

        role = current_user['role']

        if func.__name__ in ('put', 'patch'):
            if role == Role.SIMPLE_USER.value:
                kwargs['user_schema'] = SimpleUserSchemaLdapModify.__name__
                kwargs['user_fields'] = simple_user_fields
            elif role == Role.WEBADMIN.value:
                kwargs['user_schema'] = WebAdminsSchemaLdapModify.__name__
                kwargs['user_fields'] = webadmins_fields
        elif func.__name__ in 'post':
            if role == Role.WEBADMIN.value:
                kwargs['user_schema'] = WebAdminsSchemaLdapCreate.__name__
                kwargs['user_fields'] = webadmins_fields
        elif func.__name__ in 'get':
            if role == Role.WEBADMIN.value:
                kwargs['user_schema'] = WebAdminsSchemaLdapList.__name__

        res = func(*args, **kwargs)

        return res

    return wraps

