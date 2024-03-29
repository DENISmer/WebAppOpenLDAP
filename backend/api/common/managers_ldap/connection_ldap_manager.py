import pprint
import time

from ldap3 import Connection, EXTERNAL
from flask_restful import abort

from backend.api.common.decorators import error_operation_ldap
from backend.api.common.managers_ldap.ldap_manager import ManagerLDAP
from backend.api.common.user_manager import UserLdap
from backend.api.config.ldap import config


class ConnectionManagerLDAP:

    def __init__(self, user: UserLdap = None, *args, **kwargs):
        self.connection = None
        self.user = user
        self.ldap_manager = ManagerLDAP()

    @error_operation_ldap
    def __make_connection(self):
        self.connection = self.ldap_manager.make_connection(
            bind_user=self.user.dn,
            bind_password=self.user.userPassword,
            sasl_mechanism=EXTERNAL,
        )

    def create_connection(self):
        """
        This function performs create connection
        :params: self
        :return: None
        """
        self.__make_connection()

    @error_operation_ldap
    def connect(self):
        self.create_connection()
        # self.connection.open()
        if config['LDAP_USE_SSL']:
            self.connection.start_tls()
            # self.connection.tls_started()

    def bind(self, **kwargs):
        self.connection.bind(**kwargs)

    def get_connection(self):
        """
        This function performs get connection
        :return: connection
        """
        return self.connection

    def rebind(self, user: UserLdap):
        """
        This function performs rebind connection
        :return: None
        """
        self.connection.rebind(
            user=user.dn,
            password=user.userPassword,
        )

    def close(self):
        """
        This function performs close connection
        :return: None
        """
        self.connection.unbind()

    def __repr__(self):
        return (f'<Connection('
                f'user={self.connection.user}; '
                f'password={self.connection.password}; '
                f'closed={self.connection.closed} '
                f'listening={self.connection.listening}'
                f')>')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# with ConnectionManagerLDAP(user=UserLdap(dn='uid=bob,ou=people,dc=example,dc=com', password='bob')) as con:
#     con.create_connection()
#     con.connection.bind()
#     print(con.connection.result)
#     con.rebind(UserLdap(dn='uid=bob,ou=people,dc=example,dc=com', password='bob1'))
