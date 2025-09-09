import json
import time
import ssl

from flask_ldap3_login import LDAP3LoginManager
from ldap3.core import exceptions as excp
from ldap3 import MODIFY_REPLACE
from ldap3 import Tls

from api.common.exception import LDAPExceptionFlaskError
from api.conf.ldap import config as ldap_conf
from api.common.pagintor import Pagintion
from api.conf.ldap import config
from api.conf import settings


class LDAP3Manager(LDAP3LoginManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_config(config)
        self.tls_ctx = None
        self._add_tls_ctx()

    def _add_tls_ctx(self):
        if config['LDAP_USE_SSL']:
            self.tls_ctx = Tls(
                validate=ssl.CERT_REQUIRED,
                version=ssl.PROTOCOL_TLS,
                ca_certs_file=config['CERT_PATH']
            )


ldap_manager = LDAP3Manager()
for host in config['LDAP_HOSTS']:
    ldap_manager.add_server(
        hostname=host.strip(' '), port=config['LDAP_PORT'],
        use_ssl=config['LDAP_USE_SSL'], tls_ctx=ldap_manager.tls_ctx,
    )


class FormatDN:
    def format_dn(self, *args, **kwargs):
        raise NotImplementedError('Not Implemented method.')

    def compiled_sub_dn(self, prepend):
        prepend = prepend.strip()
        if prepend == '':
            return ldap_conf.get('LDAP_BASE_DN')
        return '{prepend},{base}'.format(
            prepend=prepend,
            base=ldap_conf.get('LDAP_BASE_DN')
        )

    def fetch_indetifier(self, dn):
        return dn.split(",")[0].split("=")[1]


class CommonLDAPManager:
    def __init__(self, connection):
        self.connection = connection
        self.dn = None


class RetrieveLDAPManager(CommonLDAPManager):
    def _retrieve(self, identifier, *args, **kwargs):
        try:
            attributes = kwargs.get("attributes")
            is_not_json = kwargs.get("is_not_json")

            if not attributes:
                attributes = "*"

            self.connection.search(
                search_base=self.format_dn(identifier=identifier),
                search_filter=self.search_filter,
                attributes=attributes
            )
            entries = self.connection.entries

            if not entries:
                raise LDAPExceptionFlaskError(result=404, message="No such object.")

            if is_not_json:  # if params is_not_json is passed
                return entries[0]

            json_response = json.loads(entries[0].entry_to_json())
            return json_response
        except excp.LDAPNoSuchObjectResult:
            raise LDAPExceptionFlaskError(result=404, message="No such object.")

    def retrieve(self, identifier, *args, **kwargs):
        json_response = self._retrieve(identifier, *args, **kwargs)
        return json_response


class ListLDAPManager(CommonLDAPManager):
    def list(self, *args, **kwargs):
        raise NotImplementedError('Not Implemented method list.')


class CreateLDAPManager(CommonLDAPManager):
    def create(self, dn, attributes, *args, **kwargs):
        try:
            self.connection.add(dn, attributes=attributes)
        except excp.LDAPEntryAlreadyExistsResult:
            raise LDAPExceptionFlaskError(result=400, message="Entry already exists.")
        except excp.LDAPNoSuchObjectResult as e:
            raise LDAPExceptionFlaskError(result=400, message=f"No such object {e.dn}")
        except (excp.LDAPInvalidDnError, excp.LDAPInvalidDNSyntaxResult):
            raise LDAPExceptionFlaskError(result=400, message="Invalid DN Syntax.")
        except (excp.LDAPAttributeError,
                excp.LDAPInvalidValueError,
                excp.LDAPObjectClassError) as e:
            raise LDAPExceptionFlaskError(result=400, message=e.args[0])
        except excp.LDAPConstraintViolationResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)
        except excp.LDAPObjectClassViolationResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)
        except excp.LDAPUnwillingToPerformResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)
        except excp.LDAPAttributeOrValueExistsResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)


class ModifyLDAPManager(CommonLDAPManager):
    def modify(self, identifier, changes, *args, **kwargs):
        self._retrieve(identifier)

        try:
            self.dn = self.format_dn(identifier=identifier)
            changes_converted = {}

            for key, value in changes.items():
                changes_converted[key] = [(MODIFY_REPLACE, value)]
            self.connection.modify(dn=self.dn, changes=changes_converted)

        except (excp.LDAPAttributeError,
                excp.LDAPInvalidValueError,
                excp.LDAPObjectClassError) as e:
            raise LDAPExceptionFlaskError(result=400, message=e.args[0])
        except excp.LDAPConstraintViolationResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)
        except excp.LDAPAttributeOrValueExistsResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)
        except excp.LDAPObjectClassViolationResult as e:
            raise LDAPExceptionFlaskError(result=400, message=e.message)


class DeleteLDAPManager(CommonLDAPManager):
    def delete(self, identifier, *args, **kwargs):
        self._retrieve(identifier)
        self.dn = self.format_dn(identifier=identifier)
        self.connection.delete(self.dn)


class SearchLDAPManager(CommonLDAPManager):
    def _make_search_filter(self, fields, value: str):
        search_filter = ''
        if value:
            search_filter = "(|%s)" % "".join(
                [
                    f"({field}=*{value}*)" if field not in ("uidNumber", "gidNumber") else
                    f"({field}={value})" if value.isdigit() else ""
                    for field in fields
                ]
            )
        return search_filter

    def search(self, *args, **kwargs):
        page = kwargs["page"]
        prepared_search_filter = kwargs["prepared_search_filter"]
        search_output_attributes = kwargs["search_output_attributes"]

        self.connection.search(
            search_base=ldap_conf['LDAP_BASE_DN'],
            search_filter=f"(&{prepared_search_filter}{self.search_filter})",
            attributes=search_output_attributes
        )

        entries, num_entries, num_pages = Pagintion(
            self.connection.entries, page, items_per_page=settings.ITEMS_PER_PAGE
        ).get_items()

        json_responses = []
        for entry in entries:
            json_data = json.loads(entry.entry_to_json())
            # self._delete_attrs(json_data["attributes"])
            json_responses.append(json_data)

        return {
            'items': json_responses,
            'num_pages': num_pages,
            'num_items': num_entries,
            'page': page,
        }
