import functools
import logging
import time

from flask_restful import abort

from backend.api.common.auth_http_token import auth
from backend.api.common.crypt_passwd import CryptPasswd
from backend.api.common.exceptions import form_dict_field_error, get_attribute_error_message
from backend.api.common.getting_free_id import GetFreeId
from backend.api.common.groups import Group
from backend.api.common.roles import Role
from backend.api.common.route import Route
from backend.api.common.user_manager import UserLdap
from backend.api.config import settings
from backend.api.resources.schema import schema

from ldap3.core.exceptions import (LDAPInsufficientAccessRightsResult,
                                   LDAPAttributeError,
                                   LDAPException,
                                   LDAPEntryAlreadyExistsResult,
                                   LDAPInvalidDnError,
                                   LDAPInvalidDNSyntaxResult,
                                   LDAPObjectClassError,
                                   LDAPInvalidCredentialsResult,
                                   LDAPOperationResult,
                                   LDAPObjectClassViolationResult,
                                   LDAPSocketOpenError,
                                   LDAPNoSuchObjectResult,
                                   LDAPUnwillingToPerformResult,
                                   LDAPAttributeOrValueExistsResult,
                                   LDAPNamingViolationResult)


def connection_ldap(func):
    from backend.api.common.managers_ldap.connection_ldap_manager import ConnectionManagerLDAP

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        # args[0] - self of the function
        connection = getattr(args[0], 'connection')
        if hasattr(args[0], 'connection') or not connection:
            current_user = auth.current_user()

            # print('current_user', current_user)
            if settings.NOT_AUTH:
                user = UserLdap(
                    dn='uid=bob,ou=People,dc=example,dc=com',
                    username='bob',
                    userPassword='bob',
                )
            else:
                user = UserLdap(
                    dn=current_user['dn'],
                    username=current_user['dn'],
                    userPassword=CryptPasswd(
                        password=current_user['userPassword'],
                        secret_key=bytes(settings.SECRET_KEY.encode())
                    ).decrypt()
                )

            connection = ConnectionManagerLDAP(
                user=user
            )

            setattr(args[0], 'connection', connection)

        connection.connect()

        start = time.perf_counter()
        res = func(*args, **kwargs) ####
        end = time.perf_counter()
        print(f'Time of work func {func.__name__} : {(end - start):.4f}s')

        connection.close()

        return res

    return wraps


def permission_user(miss=False):
    def decorator(func):
        @functools.wraps(func)
        def wraps(*args, **kwargs):

            current_user = auth.current_user()
            username_uid = kwargs.get('username_uid')

            if not miss:
                if current_user['uid'] != username_uid and not current_user['role'] == Role.WEBADMIN.value:
                    abort(403, message='Insufficient access rights', status=403)

            res = func(*args, **kwargs)

            return res

        return wraps

    return decorator


def permission_group(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        current_user = auth.current_user()

        # username_cn = kwargs.get('username_cn')
        if not current_user['role'] == Role.WEBADMIN.value:
            abort(403, message='Insufficient access rights', status=403)

        res = func(*args, **kwargs)

        return res

    return wraps


def error_operation_ldap(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        operation = kwargs.get('operation') or func.__name__
        object_item = kwargs.get('item')

        try:
            error = True
            res = func(*args, **kwargs)
            error = False
        except LDAPInsufficientAccessRightsResult as e:

            logging.log(logging.ERROR, e)
            abort(
                403,
                message='Insufficient access rights',
                status=403
            )
        except LDAPSocketOpenError as e:
            logging.log(logging.ERROR, str(e))
            abort(
                400,  # - 499 Client Closed Request (клиент закрыл соединение);
                message='Try again later',
                status=400
            )
        except (LDAPInvalidDnError, LDAPInvalidDNSyntaxResult) as e:
            logging.log(logging.ERROR, e)
            fields = {
                'dn': [f'Invalid field, {e}'],
            }
            abort(
                400,
                message='Invalid attributes',
                fields=fields,
                status=400
            )
        except LDAPObjectClassError as e:
            logging.log(logging.ERROR, e)
            fields = {
                'objectClass': [str(e)],
            }
            abort(
                400,
                message='Invalid attributes',
                fields=fields,
                status=400
            )
        except LDAPAttributeError as e:
            logging.log(logging.ERROR, e)
            fields = form_dict_field_error(object_item, str(e))
            abort(
                400,
                message='Invalid attributes',
                fields=fields,
                status=400
            )
        except LDAPAttributeOrValueExistsResult as e:
            logging.log(logging.ERROR, e)
            message = e.__dict__['message']
            fields = {
                key: ['Must not contain duplicate elements']
                for key in get_attribute_error_message(object_item.fields.keys(), message)
            }
            abort(
                400,
                message='Invalid attributes',
                fields=fields,
                status=400,
            )
        except LDAPEntryAlreadyExistsResult as e:
            logging.log(logging.ERROR, e)
            fields = {
                'dn': [f'An element with such a dn already exists'],
            }
            abort(
                400,
                message='Invalid attributes',
                fields=fields,
                status=400,
            )
        except LDAPInvalidCredentialsResult as e:
            logging.log(logging.ERROR, e.__dict__)
            abort(
                400,
                message='Invalid credentials',
                status=400,
            )
        except LDAPObjectClassViolationResult as e:
            logging.log(logging.ERROR, e.__dict__)
            abort(
                400,
                error='ObjectClass Violation',
                fields={
                    'objectClass': f'The required objectClass is missing, {e.__dict__["message"]}',
                },
                status=400,
            )
        except LDAPNamingViolationResult as e:
            logging.log(logging.ERROR, e)
            fields = form_dict_field_error(object_item, e.__dict__["message"])
            abort(
                400,
                errorr='Naming violation',
                fields=fields,
                status=400
            )
        except LDAPUnwillingToPerformResult as e:
            abort(
                400,
                error='Unwilling To Perform Result',
                message='Server LDAP is unwilling to perform',
                status=400,
            )
        except LDAPOperationResult as e:
            logging.log(logging.ERROR, e)
            abort(
                400,
                message=e.__dict__["message"],
                error=e.__dict__["description"],
                type=e.__dict__["type"],
                status=400
            )
        except LDAPException as e:
            logging.log(logging.ERROR, e)
            abort(
                400,
                message='Try again later1..',
                status=400
            )
        finally:
            if object_item:
                get_free_id = GetFreeId()
                get_free_id.delete_from_reserved(object_item.gidNumber)

                if hasattr(args[0], 'connection_upwrap') and error:
                    args[0].connection_upwrap.close()

        return res

    return wraps


def error_auth_ldap(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):

        try:
            res = func(*args, **kwargs)
        except LDAPNoSuchObjectResult as e:
            logging.log(logging.ERROR, e)
            abort(
                401,
                message='Invalid username or password',
                status=401
            )
        except LDAPException as e:
            logging.log(logging.ERROR, e)
            abort(
                400,
                message='Try again later',
                status=400
            )

        return res

    return wraps


def define_schema(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        username_uid = kwargs.get('username_uid')
        current_user = auth.current_user()
        role = current_user['role']
        func_name = func.__name__ if username_uid or func.__name__ == 'post' else 'list'
        print('route', kwargs.get('route'))

        if not (route := kwargs.get('route')) and Route(route.lower()):
            abort(
                404,
                error='Not Found',
                message='The requested URL was not found on the server.'
                        ' If you entered the URL manually please check your spelling and try again',
                status=404
            )

        try:
            type_group = kwargs.get('type_group')
            if type_group and Group(type_group := type_group.lower()) and schema.get(type_group):
                kwargs['webadmins_fields'] = schema[role]['fields']
                role = type_group
        except ValueError:
            abort(404, message=f'Type group not found', status=404)

        kwargs['schema'] = schema[role][func_name]['schema']
        kwargs['fields'] = schema[role]['fields']
        res = func(*args, **kwargs)

        return res

    return wraps
