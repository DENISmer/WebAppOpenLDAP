from ldap3 import Connection, EXTERNAL

from backend.api.common.ldap_manager import LDAPManager
from backend.api.common.user_manager import UserLdap
from backend.api.config.ldap import config


class ConnectionLDAP:
    _connections = {}

    def __init__(self, user: UserLdap, *args, **kwargs):
        self.user = user
        self.ldap_manager = LDAPManager()
        self._connection = None

    def create_connection(self):
        self._connection = self.ldap_manager.make_connection(
            bind_user=self.user.dn,
            bind_password=self.user.userPassword,
            sasl_mechanism=EXTERNAL,
        )

    def connect(self):
        """
        This function performs connection to OpenLDAP server
        :param self
        :return: None
        """
        self._connection: Connection = self._connections.get(
            self.user.get_username()
        )

        if not self._connection:
            conn_result = True
        else:
            conn_result = self._connection.closed or not self._connection.listening

        if conn_result:
            self.create_connection()
            self._connection.open()

            if config['LDAP_USE_SSL']:
                self._connection.tls_started()
            self._connection.bind()

            self._connections[self.user.get_username()] = self._connection

    def get_connection(self):
        return self._connection

    def show_connections(self):
        print('connection - ', self._connection.usage)
        for key, value in self._connections.items():
            print(value)
            print(f'key: {key}, value: , closed: {value.closed}, listening: {value.listening}')

    def rebind(self, user: UserLdap):
        self._connection.rebind(
            username=user.dn,
            password=user.userPassword,
        )

    def close_connection(self):
        """
        This function performs close connection
        :return: None
        """
        del self._connections[self.user.get_username()]
        self._connection.unbind()

    def __repr__(self):
        return f'Connection(user={self._connection.user}; password={self._connection.password})'
