import logging
import pprint
from typing import Dict

from flask_restful import abort
from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_DELETE
from ldap3.core.exceptions import LDAPNoSuchObjectResult

from backend.api.common.decorators import error_operation_ldap
from backend.api.common.exceptions import ItemFieldsIsNone, NotModifyItemIsNone
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from backend.api.config.ldap import config
from backend.api.config.fields import search_fields


class IniCommonManagerLDAP:
    def __init__(self, *args, **kwargs):
        connection = kwargs.get('connection')
        self.ldap_manager: ManagerLDAP = connection.ldap_manager
        self._connection = connection.connection
        self.connection_upwrap = connection


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

        # print(res)
        # abort(400, message=res['message'])
        if 'success' not in res['description']:
            # abort(400, message=res['message'])
            return None

        logging.log(logging.INFO, 'SUCCESS CREATE')

        return item

    @error_operation_ldap
    def modify(self,  item, operation, not_modify_item=None):

        if not not_modify_item:
            raise NotModifyItemIsNone('not_modify_item is None')

        serialized_data_modify = item.serialize_data(
            operation=operation,
        )
        pprint.pprint(serialized_data_modify)
        modify_dict = dict()

        for key, value in serialized_data_modify.items():
            modify_dict_value = None
            if (value is None or ((isinstance(value, list) or isinstance(value, str))
                    and (len(value) == 0 or len(str(value)) == 0)))  \
                    and getattr(not_modify_item, key) \
                    and 'create' not in item.fields[key]['required']:
                modify_dict_value = (MODIFY_DELETE, [])
            elif value:
                modify_dict_value = (
                    MODIFY_REPLACE,
                    value if isinstance(value, list) else [value]
                )
            if modify_dict_value:
                modify_dict.update({
                    key: [modify_dict_value]
                })
        pprint.pprint(modify_dict)
        self._connection.modify(
            item.dn,
            modify_dict
        )

        # print('result modify:', self._connection.result)

        res = self._connection.result
        if 'success' not in res['description']:
            # abort(400, message=res['description'])
            return None

        logging.log(logging.INFO, 'SUCCESS MODIFY')

        return item

    @error_operation_ldap
    def delete(self, item, operation='delete'):
        if item.dn:
            self._connection.delete(item.dn)

        # print('result delete:', self._connection.result)

        res = self._connection.result
        if 'success' not in res['description']:
            return None
            # abort(400, message=f'Error deleting {item.dn}')

        logging.log(logging.INFO, 'SUCCESS DELETE')

    @error_operation_ldap
    def search_by_dn(self, dn, filters, attributes=ALL_ATTRIBUTES):
        try:
            status_search = self._connection.search(
                search_base=dn,
                search_filter=filters,
                attributes=attributes,
            )
        except LDAPNoSuchObjectResult:
            return None
        if not status_search:
            return None

        return self._connection.response[0]

    def get_id_numbers(self, required_fields=None):
        if required_fields is None:
            required_fields = {'objectClass': 'person'}

        data = self.list(
            value=None,
            fields=search_fields,
            attributes=['gidNumber'],
            required_fields=required_fields,
        )

        ids = []
        for item in data:
            ids.append(item.gidNumber)

        unique_ids = set(ids)
        return unique_ids
