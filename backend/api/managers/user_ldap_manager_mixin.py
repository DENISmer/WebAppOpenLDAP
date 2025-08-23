from api.managers import user_ldap_manager as user_manager


class UserLDAPManagerMixin(
    user_manager.AttributeCleaner,
    user_manager.UserFormatDN,
    user_manager.UserRetrieveLDAPManager,
    user_manager.UserModifyLDAPManager,
    user_manager.UserDeleteLDAPManager,
    user_manager.UserCreateLDAPManager,
    user_manager.UserSearchLDAPManager,
):
    pass
