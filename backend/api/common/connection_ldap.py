import pprint

from ldap3 import Connection, EXTERNAL
from flask_restful import abort

from backend.api.common.ldap_manager import LDAPManager
from backend.api.common.user_manager import UserLdap
from backend.api.config.ldap import config


class ConnectionLDAP:
    _connections = {}

    def __init__(self, user: UserLdap, *args, **kwargs):
        self.connection = None
        self.user = user
        self.ldap_manager = LDAPManager()

    def create_connection(self):
        self.connection = self.ldap_manager.make_connection(
            bind_user=self.user.dn,
            bind_password=self.user.userPassword,
            sasl_mechanism=EXTERNAL,
        )

    @classmethod
    def _add_connection(cls, connection):
        cls._connections[connection.user] = connection

    def create_connection_new(self):
        self.connection = self.ldap_manager.make_connection(
            bind_user=self.user.dn,
            bind_password=self.user.userPassword,
            sasl_mechanism=EXTERNAL,
        )
        self._add_connection(self.connection)

        # self._connections[self.user.dn] = self.connection

    def connect_new(self):
        self.connection = self._connections.get(self.user.dn)
        if not self.connection:
            abort(403, message='Insufficient access rights.')

        self.connection.open()
        if config['LDAP_USE_SSL']:
            self.connection.tls_started()
        self.connection.bind()

    def connect(self):  # deprecated
        """
        This function performs connection to OpenLDAP server
        :param self
        :return: None
        """
        self._connection: Connection = self._connections.get(
            self.user.get_username()
        )

        if not self.connection:
            conn_result = True
        else:
            conn_result = self.connection.closed or not self.connection.listening

        if conn_result:
            self.create_connection()
            self._connection.open()

            if config['LDAP_USE_SSL']:
                self._connection.tls_started()
            self.connection.bind()

            self._connections[self.user.get_username()] = self.connection

    def get_connection(self):
        return self._connection

    def show_connections(self):
        # print('connection - ', self.connection.usage)
        print('#'*10, 'CONNECTIONS', '#'*10)
        for id, (key, value) in enumerate(self._connections.items()):
            print(f'ID - {id} ''connection')
            print(f'key: {key}, closed: {value.closed}, listening: {value.listening}, value: |')
            pprint.pprint(value)
        print('END')

    def rebind(self, user: UserLdap):
        self.connection.rebind(
            username=user.dn,
            password=user.userPassword,
        )

    def close_connection(self):  # deprecated
        """
        This function performs close connection
        :return: None
        """
        del self._connections[self.user.get_username()]
        self.connection.unbind()

    def close(self):
        self.connection.unbind()
        # del self._connections[self.user.dn]

    def clear(self):
        del self._connections[self.user.dn]

    def __repr__(self):
        return f'<Connection(user={self._connection.user}; password={self._connection.password})>'
