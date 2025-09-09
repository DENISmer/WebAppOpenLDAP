from api.managers import group_ldap_manager as group_manager


class GroupLDAPManagerMixin(
    group_manager.GroupFormatDN,
    group_manager.GroupRetrieveLDAPManager,
    group_manager.GroupCreateLDAPManager,
    group_manager.GroupModifyLDAPManager,
    group_manager.GroupDeleteLDAPManager,
    group_manager.GroupSearchLDAPManager
):
    pass
