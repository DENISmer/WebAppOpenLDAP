import time

from backend.api.common.decorators import error_auth_ldap
from backend.api.common.managers_ldap.connection_ldap_manager import ConnectionManagerLDAP
from backend.api.common.user_manager import UserLdap


class AuthenticationManagerLDAP:
    def __init__(self, user: UserLdap, connection: ConnectionManagerLDAP, *args, **kwargs):
        self.user = user
        self.connection = connection

    @error_auth_ldap
    def authenticate(self, *args, **kwargs) -> UserLdap:
        user_dn = '{rdn}={username},{user_search_dn}'.format(
            rdn=self.connection.ldap_manager.config.get('LDAP_USER_LOGIN_ATTR'),
            username=self.user.get_username(),
            user_search_dn=self.connection.ldap_manager.full_user_search_dn,
        )
        self.user.dn = user_dn
        self.user.uid = self.user.get_username()

        self.connection.rebind(user=self.user)

        return self.user
