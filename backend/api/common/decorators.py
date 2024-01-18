import functools

from flask_restful import abort

from backend.api.common.auth_http_token import auth


def connection_ldap(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        print('Iam decorator')
        kwargs['connection'] = 'connection_user'
        res = func(*args, **kwargs)

        return res

    return wraps


def permission_user(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        current_user = auth.current_user()
        username_uid = kwargs['username_uid']

        if current_user['uid'] != username_uid:
            abort(403)

        if not current_user['webadmins'] and current_user['uid'] != username_uid:
            abort(403)

        res = func(*args, **kwargs)

        return res

    return wraps

