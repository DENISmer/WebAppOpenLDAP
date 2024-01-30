from backend.api.common.managers_ldap.common_ldap_manager import IniCommonManagerLDAP
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP


class AuthenticationManagerLDAP:
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.ldap_manager = ManagerLDAP()

    def authenticate(self):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username(),
            password=self.user.userPassword,
        )

        return response  # *.status: 2 - success, 1 - failed