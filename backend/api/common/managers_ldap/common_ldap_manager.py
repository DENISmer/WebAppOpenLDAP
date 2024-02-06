import pprint
from typing import Dict

from flask_restful import abort
from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_DELETE

from backend.api.common.decorators import error_operation_ldap
from backend.api.common.exceptions import ItemFieldsIsNone
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from backend.api.config.ldap import config


class IniCommonManagerLDAP:
    def __init__(self, *args, **kwargs):
        connection = kwargs.get('connection')
        self.ldap_manager: ManagerLDAP = connection.ldap_manager
        self._connection = connection.connection
        self.connection_con = connection.connection


class CommonManagerLDAP(IniCommonManagerLDAP):

    def list(self, *args, **kwargs):
        raise NotImplementedError('Not Implemented method list.')

    def item(self, *args, **kwargs):
        raise NotImplementedError('Not Implemented method get_item.')

    @error_operation_ldap
    def search(
        self,
        value,
        fields: Dict[str, str],
        attributes=ALL_ATTRIBUTES,
        required_fields: Dict[str, str] = None,
        **kwargs,
    ) -> list:

        search_filter = ''
        required_filter = ''

        if not value and not required_fields:
            return []

        if value:
            search_filter = '(|%s)' % "".join(
                [
                    f'({field}={fields[field] % value})' for field in fields
                    if (fields[field] == '%d' and str(value).isdigit() and (value := int(value)))
                       or ('%s' in fields[field])
                ]
            )

        if required_fields:
            required_filter = '(|%s)' % "".join(
                [
                    f'({key}={value_d})' for key, value_d in required_fields.items()
                ]
            )

        common_filter = '(&%s%s)' % (
            search_filter,
            required_filter
        )
        # print(common_filter)
        # exception connection is open!!!!!
        status_search = self._connection.search(
            search_base=config['LDAP_BASE_DN'],
            search_filter=common_filter,
            attributes=attributes,
        )
        if not status_search:
            return []
        return self._connection.response

    @error_operation_ldap
    def create(self, item, operation):
        if item.fields is None:
            raise ItemFieldsIsNone('Item fields is none.')

        self._connection.add(
            item.dn,
            attributes=item.serialize_data(
                operation=operation
            )
        )

        res = self._connection.result

        print(res)
        # abort(400, message=res['message'])
        if 'success' not in res['description']:
            abort(400, message=res['message'])
        print('Success')

        return item

    # @error_operation_ldap
    def modify(self,  item, operation, not_modify_item=None):

        serialized_data_modify = item.serialize_data(
            operation=operation,
        )

        modify_dict = dict()

        for key, value in serialized_data_modify.items():
            if (value is None or ((isinstance(value, list) or isinstance(value, str)) and (len(value) == 0 or len(str(value)) == 0))) \
                    and getattr(not_modify_item, key) \
                    and 'create' not in item.fields[key]['required']:
                tmp_modify = MODIFY_DELETE
                tmp_value = []
            else:
                tmp_modify = MODIFY_REPLACE
                tmp_value = value if type(value) == list else [value]

            modify_dict.update({
                key: [(
                    tmp_modify,
                    tmp_value
                )]
            })

        self._connection.modify(
            item.dn,
            modify_dict
        )

        print('result modify:', self._connection.result)

        res = self._connection.result
        if 'success' not in res['description']:
            abort(400, message=res['description'])

        return item

    @error_operation_ldap
    def delete(self, item, operation='delete'):
        if item.dn:
            self._connection.delete(item.dn)

        print('result delete:', self._connection.result)

        res = self._connection.result
        if 'success' not in res['description']:
            abort(400, message=f'Error deletion {item.dn}')

    def search_by_dn(self, dn, filters, attributes=ALL_ATTRIBUTES):
        status_search = self._connection.search(
            search_base=dn,
            search_filter=filters,
            attributes=attributes,
        )
        if not status_search:
            return None
        print(self._connection.response)
        return self._connection.response[0]
