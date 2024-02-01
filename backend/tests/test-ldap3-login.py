
from flask_ldap3_login import LDAP3LoginManager
import time
from ldap3 import ALL_ATTRIBUTES

config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostname of your LDAP Server
config['LDAP_HOST'] = '0.0.0.0'

# Base DN of your directory
config['LDAP_BASE_DN'] = 'dc=example,dc=com'

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'ou=People'

# Groups DN to be prepended to the Base DN
# config['LDAP_GROUP_DN'] = 'ou=groups'


# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
config['LDAP_USER_LOGIN_ATTR'] = 'uid'
config['LDAP_SEARCH_FOR_GROUPS'] = False

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = None

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = None

# Setup a LDAP3 Login Manager.
ldap_manager = LDAP3LoginManager()

# Init the mamager with the config since we aren't using an app
ldap_manager.init_config(config)

# Check if the credentials are correct
response = ldap_manager.authenticate('bob', 'bob')
print('-- User info:')
print(response.user_info)
for item in response.user_info:
    print(item, ':', response.user_info[f'{item}'])
print('-- Other params:')
print(response.user_dn)
print(response.user_id)
print(response.status)
print(response.status.name)
print(response.status.value)

response = ldap_manager.authenticate('john', 'john')
print(response.status)
print(response.status.name)
print(response.status.value)


_connection = ldap_manager.make_connection(
    bind_user='bob',
    bind_password='bob',
)
_connection.open()
print(_connection.listening)
print(_connection.closed)
connection_search = _connection.search(
    'dc=example,dc=com',
    '(objectClass=person)',
    attributes=ALL_ATTRIBUTES
)
# print(connection_search)
# print(_connection.entries)
# print(ldap_manager.connection.entries)

time.sleep(2)

print(_connection.receive_timeout)
# _connection.unbind()

connection_search = _connection.search(
    'dc=example,dc=com',
    '(&(cn=webadmins)(objectClass=groupOfNames))',
    attributes=ALL_ATTRIBUTES
)
print(connection_search)
print(_connection.entries)