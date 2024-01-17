import functools


def connection_ldap(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        print('Iam decorator')
        kwargs['connection'] = 'connection_user'
        res = func(*args, **kwargs)

        return res

    return wraps
