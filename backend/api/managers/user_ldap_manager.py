import json
import time

from ldap3.core import exceptions as excp

from api.managers.group_ldap_manager_mixin import GroupLDAPManagerMixin
from api.managers import ldap_manager as managers
from api.conf.ldap import config as ldap_conf
from api.conf import settings


class AttributeCleaner:
    def delete_attrs(self, data: dict):
        keys = ["userPassword", "jpegPhoto"]
        for key in keys:
            if data.get(key):
                del data[key]


class UserFormatDN(managers.FormatDN):
    def format_dn(self, *args, **kwargs):
        identifier = kwargs["identifier"]

        dn = "uid={uid},{base}".format(
            uid=identifier, base=self.compiled_sub_dn(ldap_conf.get("LDAP_USER_DN"))
        )

        return dn


class UserRetrieveLDAPManager(managers.RetrieveLDAPManager):
    search_filter = "(objectClass=Person)"

    def retrieve(self, identifier, *args, **kwargs):
        json_response = self._retrieve(identifier, *args, **kwargs)
        self.delete_attrs(json_response["attributes"])
        return json_response


class UserModifyLDAPManager(managers.ModifyLDAPManager):
    search_filter_person = "(objectClass=Person)"

    def modify(self, identifier, changes, *args, **kwargs):
        super().modify(identifier, changes, *args, **kwargs)

        gid_number = changes.get("gidNumber")
        if gid_number:
            try:
                GroupLDAPManagerMixin(self.connection).modify(
                    identifier,
                    changes={
                        "gidNumber": gid_number
                    }
                )
            except excp.LDAPNoSuchObjectResult:
                pass


class UserDeleteLDAPManager(managers.DeleteLDAPManager):
    search_filter = "(objectClass=Person)"

    def delete(self, identifier, *args, **kwargs):

        super().delete(identifier, *args, **kwargs)

        try:
            GroupLDAPManagerMixin(self.connection).delete(identifier)
        except excp.LDAPNoSuchObjectResult:
            pass


class UserCreateLDAPManager(managers.CreateLDAPManager):

    def create(self, dn, attributes, *args, **kwargs):
        super().create(dn, attributes, *args, **kwargs)

        uid = self.fetch_indetifier(dn)
        try:
            group_mixin = GroupLDAPManagerMixin(self.connection)
            group_mixin.create(
                dn=group_mixin.format_dn(identifier=uid),
                attributes={
                    "cn": [uid],
                    "gidNumber": [attributes["gidNumber"][0]],
                    "memberUid": [uid],
                    "objectClass": ["posixGroup"]
                }
            )
        except excp.LDAPEntryAlreadyExistsResult:
            pass


class UserSearchLDAPManager(managers.SearchLDAPManager):
    search_filter = "(objectClass=Person)"

    def search(self, value, page, *args, **kwargs):
        prepared_search_filter = self._make_search_filter(settings.SEARCH_FIELDS, value)

        return super().search(page=page,
                              prepared_search_filter=prepared_search_filter,
                              search_output_attributes=settings.SEARCH_OUTPUT_ATTRIBUTES)
