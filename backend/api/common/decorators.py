import functools
import pprint
import logging

from flask_restful import abort

from backend.api.common.auth_http_token import auth
from backend.api.common.exceptions import get_attribute_error_fields
from backend.api.common.managers_ldap.connection_ldap_manager import ConnectionManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.user_manager import UserLdap
from backend.api.config.fields import (simple_user_fields,
                                       webadmins_fields,
                                       webadmins_cn_group_fields)
from backend.api.resources.schema import (SimpleUserSchemaLdapModify,
                                          WebAdminsSchemaLdapModify,
                                          WebAdminsSchemaLdapCreate,
                                          WebAdminsSchemaLdapList,
                                          CnGroupSchemaModify,
                                          CnGroupSchemaCreate,
                                          CnGroupSchemaList)

from ldap3.core.exceptions import (LDAPInsufficientAccessRightsResult,
                                   LDAPAttributeError,
                                   LDAPException,
                                   LDAPEntryAlreadyExistsResult,
                                   LDAPInvalidDnError,
                                   LDAPInvalidDNSyntaxResult,
                                   LDAPObjectClassError,
                                   LDAPInvalidCredentialsResult,
                                   LDAPOperationResult)


def connection_ldap(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        # args[0] - self of the function
        connection = getattr(args[0], 'connection')
        if hasattr(args[0], 'connection') or not connection:
            current_user = auth.current_user()
            print('current_user', current_user)
            connection = ConnectionManagerLDAP(
                # UserLdap(
                #     dn=current_user['dn'],
                # )
                UserLdap(
                    dn='uid=bob,ou=People,dc=example,dc=com',
                    username='bob',
                    userPassword='bob',
                )
            )

            setattr(args[0], 'connection', connection)
        connection.show_connections()
        connection.create_connection_new()
        connection.connect_new()

        res = func(*args, **kwargs)
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
                    abort(403, message='Insufficient access rights.')
            else:
                username_uid = current_user['uid']

            role = current_user['role']

            if func.__name__ in ('put', 'patch', 'get') and username_uid:
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

    return decorator


def permission_group(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):
        current_user = auth.current_user()

        username_cn = kwargs.get('username_cn')
        if not current_user['role'] == Role.WEBADMIN.value:
            abort(403, message='Insufficient access rights.')

        role = current_user['role']
        if kwargs.get('type_group') == 'posixgroup':
            if func.__name__ in ('put', 'patch', 'get') and username_cn:
                if role == Role.WEBADMIN.value:
                    kwargs['group_schema'] = CnGroupSchemaModify.__name__
                    kwargs['group_fields'] = webadmins_cn_group_fields
                    kwargs['webadmins_user_fields'] = webadmins_fields
            elif func.__name__ in 'post':
                if role == Role.WEBADMIN.value:
                    kwargs['group_schema'] = CnGroupSchemaCreate.__name__
                    kwargs['group_fields'] = webadmins_cn_group_fields
                    kwargs['webadmins_user_fields'] = webadmins_fields
            elif func.__name__ in 'get':
                if role == Role.WEBADMIN.value:
                    kwargs['group_schema'] = CnGroupSchemaList.__name__
                    kwargs['webadmins_user_fields'] = webadmins_fields
        else:
            abort(404, message='Type group not found.')

        res = func(*args, **kwargs)

        return res

    return wraps


def error_operation_ldap(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):
        operation = kwargs['operation']
        object_item = kwargs['item']

        try:
            res = func(*args, **kwargs)
        except LDAPInsufficientAccessRightsResult as e:
            print('##LDAPInsufficientAccessRightsResult##')
            pprint.pprint(e)
            logging.log(logging.ERROR, e)
            abort(403, message='Insufficient access rights')
        except (LDAPInvalidDnError, LDAPInvalidDNSyntaxResult) as e:
            print('##LDAPInvalidDnError, LDAPInvalidDNSyntaxResult##')
            print(e)
            logging.log(logging.ERROR, e)
            fields = {
                'fields': {
                    'dn': f'Invalid field, {e}',
                }
            }
            abort(400, message=fields)
        except LDAPObjectClassError as e:
            print('##LDAPObjectClassError##')
            print(str(e))
            print(e.__dict__)
            logging.log(logging.ERROR, e)
            fields = {
                'fields': {
                    'objectClass': str(e),
                }
            }
            abort(400, message=fields)
        except LDAPAttributeError as e:
            print('##LDAPATTRERROR##')
            pprint.pprint(e.__dict__)
            pprint.pprint(e)
            logging.log(logging.ERROR, e)
            fields = {
                'fields': {
                    item: str(e)
                    for item in get_attribute_error_fields(
                        list(object_item.fields.keys()), str(e)
                    )
                }
            }
            abort(400, message=fields)
        except LDAPEntryAlreadyExistsResult as e:
            print('##LDAPEntryAlreadyExistsResult##')
            pprint.pprint(e.__dict__)
            logging.log(logging.ERROR, e)
            fields = {
                'fields': {
                    'dn': f'An element with such a dn already exists',
                }
            }
            abort(400, message=fields)
        except LDAPInvalidCredentialsResult as e:
            logging.log(logging.ERROR, e.__dict__)
            abort(400, message='Invalid credentials')
        except LDAPOperationResult as e:
            print('##LDAPOperationResult##')
            logging.log(logging.ERROR, e)
            print(e.__dict__)
            abort(
                400,
                message=f'The operation {operation} has not '
                        f'been completed (description={e.__dict__["description"]},'
                        f' message={e.__dict__["message"]})')
        except LDAPException as e:
            print('##LDAPException##')
            # pprint.pprint(self._connection.result)
            pprint.pprint(e.__dict__)
            pprint.pprint(e.args)
            pprint.pprint(e)
            logging.log(logging.ERROR, e)
            abort(400, message='Failed 500. Unhandled errors')

        return res

    return wraps
