from backend.api.common.decorators import error_auth_ldap
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP


class AuthenticationManagerLDAP:
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.ldap_manager = ManagerLDAP()

    @error_auth_ldap
    def authenticate(self, *args, **kwargs):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username(),
            password=self.user.userPassword,
        )
        return response  # *.status: 2 - success, 1 - failed