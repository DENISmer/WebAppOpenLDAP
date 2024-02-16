from enum import Enum


class Route(Enum):
    common_route = '/api/v1'
    AUTH = f'{common_route}/auth/token'
    USERS = f'{common_route}/users'
    GROUPS = f'{common_route}/groups'


# Authentication
data_user_auth_bob_webadmins = {
    "username": "bob",
    "userPassword": "bob"
}
data_user_auth_john_simple_user = {
    "username": "john",
    "userPassword": "johnldap"
}
data_user_auth_bob_invalid_data = {
    "username": "bob1",
    "userPassword": "bob1"
}
data_user_auth_more_field = {
    "username": "bob1",
    "userPassword": "bob1",
    "password": "asdasdas",
    "gesoc": "dasdasd"
}
data_user_auth_missing_field = {
    "username": "bob1",
}
data_user_auth_empty_field = {
    "username": "",
    "userPassword": "",
}


# GET
# Default users: bob is webadmins, john

data_user_get_bob_webadmins = {
    'cn': 'Bob Bondy',
    'displayName': 'Bob Bondy',
    'dn': 'uid=bob,ou=People,dc=example,dc=com',
    'gidNumber': 10001,
    'givenName': 'bob',
    'homeDirectory': '/home/bob',
    'loginShell': '/bin/bash',
    'mail': [],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount',
                 'ldapPublicKey'],
    'postalCode': None,
    'sn': 'Bondy',
    'sshPublicKey': [],
    'st': None,
    'street': None,
    'uid': 'bob',
    'uidNumber': 10001
}

data_user_get_john_simple_user = {
    'cn': 'John Doe',
    'displayName': 'John Doe',
    'dn': 'uid=john,ou=People,dc=example,dc=com',
    'gidNumber': 10000,
    'givenName': 'John',
    'homeDirectory': '/home/john',
    'loginShell': '/bin/bash',
    'mail': [],
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount'],
    'postalCode': None,
    'sn': 'Doe',
    'sshPublicKey': [],
    'st': None,
    'street': None,
    'uid': 'john',
    'uidNumber': 10000
}


data_user_get_not_found = {
    'uid': 'boboob'
}


# POST
data_user_post_margo_simple_user = {
    'cn': 'Margo Rob',
    'displayName': 'Margo Rob',
    'dn': 'uid=margo,ou=People,dc=example,dc=com',
    'gidNumber': 10003,
    'givenName': 'Margo',
    'homeDirectory': '/home/margo',
    'loginShell': '/bin/bash',
    'mail': [],
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount', 'ldapPublicKey'],
    'postalCode': 123123,
    'sn': 'Margo',
    'sshPublicKey': [],
    'st': 'grenlandy',
    'street': 'groove street',
    'uid': 'margo',
    'uidNumber': 10003
}
