import time
import functools

from flask_restful import abort
from ldap3 import EXTERNAL
from ldap3.core import exceptions as excp

from api.managers.ldap_manager import ldap_manager
from api.common.auth_http_token import auth
from api.conf.ldap import config as ldap_conf
from api.common.crypt_passwd import CryptPasswd
from api.conf import settings


def connection_ldap(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        print(f"id ldapmanager resource get: {id(ldap_manager)}")

        connection = getattr(args[0], 'connection')

        if not connection:
            current_user = auth.current_user()
            password = CryptPasswd(
                password=current_user['userPassword'],
                secret_key=bytes(settings.SECRET_KEY.encode())
            ).decrypt()
            connection = ldap_manager.make_connection(
                bind_user=f"uid={current_user['uid']},{ldap_conf['LDAP_USER_DN']},{ldap_conf['LDAP_BASE_DN']}",
                bind_password=password,
                sasl_mechanism=EXTERNAL
            )

        connection.bind()

        setattr(args[0], 'connection', connection)

        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Time of work func {func.__name__} : {(end - start):.4f}s')

        print(f"id con: {id(connection)}")

        connection.unbind()

        return res
    return wraps


def error_operation_ldap(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):

        try:
            res = func(*args, **kwargs)
            return res
        except (excp.LDAPInsufficientAccessRightsResult, excp.LDAPInvalidCredentialsResult) as e:
            abort(403, message="Insufficient access rights", status=403)
        except excp.LDAPOperationResult as e:
            abort(e.result, message=e.message, status=e.result)
        except excp.LDAPException as e:
            abort(500, message=f"Этот исключение является заглушкой {e.args[0]}", status=500)

    return wraps
