from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from ldap3.core.exceptions import LDAPNoSuchObjectResult
from flask_restful import abort


class AuthenticationManagerLDAP:
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.ldap_manager = ManagerLDAP()

    def authenticate(self):
        try:
            response = self.ldap_manager.authenticate(
                username=self.user.get_username(),
                password=self.user.userPassword,
            )
        except LDAPNoSuchObjectResult as e:
            abort(400, message='User not found', status=400)

        return response  # *.status: 2 - success, 1 - failed