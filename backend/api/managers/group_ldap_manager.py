
from api.managers import ldap_manager as managers
from api.conf.ldap import config as ldap_conf
from api.conf import settings


class GroupFormatDN(managers.FormatDN):
    def format_dn(self, *args, **kwargs):
        identifier = kwargs["identifier"]

        dn = "cn={uid},{base}".format(
            uid=identifier, base=self.compiled_sub_dn(ldap_conf.get("LDAP_GROUP_DN"))
        )

        return dn


class GroupRetrieveLDAPManager(managers.RetrieveLDAPManager):
    search_filter = ldap_conf["LDAP_GROUP_OBJECT_FILTER"]


class GroupModifyLDAPManager(managers.ModifyLDAPManager):
    search_filter = ldap_conf["LDAP_GROUP_OBJECT_FILTER"]


class GroupDeleteLDAPManager(managers.DeleteLDAPManager):
    search_filter = ldap_conf["LDAP_GROUP_OBJECT_FILTER"]


class GroupCreateLDAPManager(managers.CreateLDAPManager):
    pass


class GroupSearchLDAPManager(managers.SearchLDAPManager):
    search_filter = ldap_conf["LDAP_GROUP_OBJECT_FILTER"]

    def search(self, value, page, *args, **kwargs):
        prepared_search_filter = self._make_search_filter(settings.GROUP_SEARCH_FIELDS, value)
        return super().search(page=page,
                              prepared_search_filter=prepared_search_filter,
                              search_output_attributes=['*'])
