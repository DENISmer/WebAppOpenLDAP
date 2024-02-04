import pprint

from ldap3 import Connection, EXTERNAL
from flask_restful import abort

from backend.api.common.decorators import error_operation_ldap
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from backend.api.common.user_manager import UserLdap
from backend.api.config.ldap import config


class ConnectionManagerLDAP:
    _connections = {}

    def __init__(self, user: UserLdap, *args, **kwargs):
        self.connection = None
        self.user = user
        self.ldap_manager = ManagerLDAP()

    # @error_operation_ldap
    def make_connection(self):
        self.connection = self.ldap_manager.make_connection(
            bind_user=self.user.dn,
            bind_password=self.user.userPassword,
            sasl_mechanism=EXTERNAL,
        )

    @classmethod
    def _add_connection(cls, connection):
        cls._connections[connection.user] = connection

    def create_connection(self):
        self.make_connection()
        self._add_connection(self.connection)

        # self._connections[self.user.dn] = self.connection

    def connect(self):
        self.connection = self._connections.get(self.user.dn)
        if not self.connection:
            abort(403, message='Unauthorized Access', status=403)#'Insufficient access rights.')

        self.connection.open()
        if config['LDAP_USE_SSL']:
            self.connection.tls_started()
        self.connection.bind()

    def get_connection(self):
        return self.connection

    def show_connections(self):
        # print('connection - ', self.connection.usage)
        print('#'*10, 'CONNECTIONS', '#'*10)
        for id, (key, value) in enumerate(self._connections.items()):
            print(f'ID - {id} ''connection')
            print(f'key: {key}, closed: {value.closed}, listening: {value.listening}, value: |')
            pprint.pprint(value)
        print('END')

    def rebind(self, user: UserLdap):
        """
        This function performs rebind connection
        :return: None
        """
        self.connection.rebind(
            username=user.dn,
            password=user.userPassword,
        )

    def close(self):
        """
        This function performs close connection
        :return: None
        """
        self.connection.unbind()
        # del self._connections[self.user.dn]

    def clear(self):
        """
        This function performs clear connection
        :return: None
        """
        del self._connections[self.user.dn]

    def __repr__(self):
        return f'<Connection(user={self.connection.user}; password={self.connection.password})>'
