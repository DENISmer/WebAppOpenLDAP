import functools

from flask_restful import abort

from backend.api.common.auth_http_token import auth
from backend.api.common.ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.user_manager import User


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
        username_uid = kwargs['username_uid']

        if current_user['uid'] != username_uid and not current_user['role'] == Role.WEBADMIN.value:
            abort(403, message='Insufficient access rights')

        res = func(*args, **kwargs)

        return res

    return wraps

