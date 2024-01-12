from ldap3 import ALL_ATTRIBUTES

from flask_ldap3_login import LDAP3LoginManager

from backend.api.common.exceptions import CouldNotCreateConnection
from backend.api.common.user_manager import User
from backend.api.config.ldap import config

# Setup a LDAP3 Login Manager.
# ldap_manager = LDAP3LoginManager()
#
# # Init the mamager with the config since we aren't using an app
# ldap_manager.init_config(config)
#
# # Check if the credentials are correct
# response = ldap_manager.authenticate('bob', 'bob')
# print('-- User info:')
# print(response.user_info)
# for item in response.user_info:
#     print(item, ':', response.user_info[f'{item}'])
# print('-- Other params:')
# print(response.user_dn)
# print(response.user_id)
# print(response.status)
# print(response.status.name)
# print(response.status.value)
#
# response = ldap_manager.authenticate('john', 'johnldap')
# print(response.status)


class MetaSingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class LdapManager(LDAP3LoginManager, metaclass=MetaSingleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_config(config)


class LdapConnection:
    def __init__(self, user: User):
        self.ldap_manager = LdapManager()
        self.user = user
        self.status_auth = 1

    def open_connection(self):
        if not self.status_auth == 2:
            raise CouldNotCreateConnection(f'Authentication failed, status {self.status_auth}')

        self._connection = self.ldap_manager.make_connection(
            bind_user=self.user.uid,
            bind_password=self.user.userPassword,
        )
        self._connection.open()

    def _authenticate(self):
        status = self._connection.authentication(
            self.user.uid,
            self.user.userPassword,
        )
        self.status_auth = status.value


ldap_manager = LdapManager()
print('ldap_manager', id(ldap_manager))

ldap_manager1 = LdapManager()
print('ldap_manager1', id(ldap_manager1))

l = ldap_manager.authenticate('bob', 'bob')
print('bob auth', l.status)
l1 = ldap_manager.authenticate('john', 'john')
print('dn', l1.user_dn)
print('john auth', l1.status)

connection = ldap_manager.make_connection(
    bind_user='john',
    bind_password='john'
)
connection.open()
print(connection.listening)
# print(connection.)
connection_search = connection.search(
    'dc=example,dc=com',
    '(objectClass=person)',
    attributes=ALL_ATTRIBUTES,
)
# print(connection.entries)
