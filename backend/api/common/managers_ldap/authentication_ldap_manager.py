from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP


class AuthenticationManagerLDAP(UserManagerLDAP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username(),
            password=self.user.userPassword,
        )

        return response  # *.status: 2 - success, 1 - failed