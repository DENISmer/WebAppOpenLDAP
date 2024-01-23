from backend.api.common.user_ldap_manager import UserManagerLDAP


class AuthenticationLDAP(UserManagerLDAP):

    def authenticate(self):
        response = self.ldap_manager.authenticate(
            username=self.user.get_username(),
            password=self.user.userPassword,
        )

        # if response.status.value == 2:
        #     users[self.user.get_username_uid()] = self.user.userPassword

        return response  # *.status: 2 - success, 1 - failed