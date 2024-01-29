from backend.api.common.connection_ldap import ConnectionLDAP
from backend.api.common.ldap_manager import LDAPManager
from backend.api.common.user_ldap_manager import UserManagerLDAP
from backend.api.common.user_manager import UserLdap


class AuthenticationLDAP(UserManagerLDAP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username(),
            password=self.user.userPassword,
        )

        return response  # *.status: 2 - success, 1 - failed