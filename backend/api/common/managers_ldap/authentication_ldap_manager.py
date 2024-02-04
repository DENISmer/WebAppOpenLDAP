from backend.api.common.decorators import error_operation_ldap
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from ldap3.core.exceptions import LDAPNoSuchObjectResult
from flask_restful import abort


class AuthenticationManagerLDAP:
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.ldap_manager = ManagerLDAP()

    @error_operation_ldap
    def authenticate(self, *args, **kwargs):
        # try:
        response = self.ldap_manager.authenticate(
            username=self.user.get_username(),
            password=self.user.userPassword,
        )
        # except LDAPNoSuchObjectResult as e:
        #     abort(400, message='User not found', status=400)

        return response  # *.status: 2 - success, 1 - failed