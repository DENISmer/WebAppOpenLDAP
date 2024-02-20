from enum import Enum


class Route(Enum):
    common_route = '/api/v1'
    AUTH = f'{common_route}/auth/token'
    USERS = f'{common_route}/users'
    GROUPS = f'{common_route}/groups'
    FREE_IDS = f'{common_route}/free-ids'


# Authentication
data_user_auth_bob_webadmins = {
    "username": "bob",
    "userPassword": "bob"
}
data_user_auth_john_simple_user = {
    "username": "john",
    "userPassword": "johnldap"
}
data_user_auth_rambo_simple_user = {
    "username": "rambo",
    "userPassword": "12345678"
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
    'dn': 'uid=bob,ou=people,dc=example,dc=com',
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
    'uidNumber': 10001,
    'jpegPhotoPath': None
}
data_user_get_john_simple_user = {
    'cn': 'John Doe',
    'displayName': 'John Doe',
    'dn': 'uid=john,ou=people,dc=example,dc=com',
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
    'uidNumber': 10000,
    'jpegPhotoPath': None
}
data_user_get_not_found = {
    'uid': 'boboob'
}


# POST

data_user_post_margo_simple_user = {
    'cn': 'Margo Rob',
    'displayName': 'Margo Rob',
    'dn': 'uid=margo,ou=people,dc=example,dc=com',
    'gidNumber': 10003,
    'givenName': 'Margo',
    'homeDirectory': '/home/margo',
    'loginShell': '/bin/bash',
    'mail': ['margo@mail.ru', 'margo1@mail.ru'],
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount', 'ldapPublicKey'],
    'postalCode': 123123,
    'sn': 'Margo',
    'sshPublicKey': ['ssh-rsa asdasdas='],
    'st': 'grenlandy',
    'street': 'groove street',
    'uid': 'margo',
    'uidNumber': 10003,
    'jpegPhotoPath': None
}
data_user_post_james_data_not_required_fields_is_null_simple_user = {
    'cn': 'James Raf',
    'displayName': None,
    'dn': 'uid=james,ou=people,dc=example,dc=com',
    'gidNumber': None,
    'givenName': None,
    'homeDirectory': '/home/james',
    'loginShell': None,
    'mail': None,
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount', 'ldapPublicKey'],
    'postalCode': None,
    'sn': 'James',
    'sshPublicKey': None,
    'st': None,
    'street': None,
    'uid': 'james',
    'uidNumber': None,
    'userPassword': '12341234'
}
data_user_post_data_all_fields_is_null = {
    'cn': None,
    'displayName': None,
    'dn': None,
    'gidNumber': None,
    'givenName': None,
    'homeDirectory': None,
    'loginShell': None,
    'mail': None,
    'objectClass': None,
    'postalCode': None,
    'sn': None,
    'sshPublicKey': None,
    'st': None,
    'street': None,
    'uid': None,
    'uidNumber': None,
    'userPassword': None
}
data_user_post_data_all_fields_is_list = {
    'cn': [],
    'displayName': [],
    'dn': [],
    'gidNumber': [],
    'givenName': [],
    'homeDirectory': [],
    'loginShell': [],
    'mail': [],
    'objectClass': [],
    'postalCode': [],
    'sn': [],
    'sshPublicKey': [],
    'st': [],
    'street': [],
    'uid': [],
    'uidNumber': [],
    'userPassword': []
}
data_user_post_data_all_fields_is_list_with_none_empty_row = {
    'cn': ["", None],
    'displayName': ["", None],
    'dn': ["", None],
    'gidNumber': ["", None],
    'givenName': ["", None],
    'homeDirectory': ["", None],
    'loginShell': ["", None],
    'mail': ["", None],
    'objectClass': ["", None],
    'postalCode': ["", None],
    'sn': ["", None],
    'sshPublicKey': ["", None],
    'st': ["", None],
    'street': ["", None],
    'uid': ["", None],
    'uidNumber': ["", None],
    'userPassword': ["", None]
}
data_user_post_james_data_required_fields_simple_user = {
    'cn': 'James Raf',
    'dn': 'uid=james,ou=people,dc=example,dc=com',
    'homeDirectory': '/home/james',
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount', 'ldapPublicKey'],
    'sn': 'James',
    'uid': 'james',
    'userPassword': '12341234'
}
data_user_post_james_data_required_fields_simple_user_response = {
    'cn': 'James Raf',
    'displayName': None,
    'dn': 'uid=james,ou=people,dc=example,dc=com',
    'gidNumber': 10002,
    'givenName': None,
    'homeDirectory': '/home/james',
    'loginShell': None,
    'mail': [],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount',
                 'ldapPublicKey'],
    'postalCode': None,
    'sn': 'James',
    'sshPublicKey': [],
    'st': None,
    'street': None,
    'uid': 'james',
    'uidNumber': 10002,
    'jpegPhotoPath': None
}
data_user_post_james_data_incorrect_fields_simple_user = {
    'cn': 'James Raf',
    'displayName': 'None',
    'dn': 'uid=jamesou=peopledc=exampledc=com',
    'gidNumber': 10002,
    'givenName': 'None',
    'homeDirectory': '/home/james',
    'loginShell': 'None',
    'mail': [],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount'],
    'postalCode': 344134,
    'sn': 'James',
    'sshPublicKey': ["ssh-rsa dasdffff= fsdf"],
    'st': 'None',
    'street': 'None',
    'uid': 'james1',
    'uidNumber': 10002,
    'userPassword': 'asdasdasdasd'
}
data_user_post_james_data_less_10000_simple_user = {
    'cn': 'James Raf',
    'displayName': 'None',
    'dn': 'uid=james,ou=people,dc=example,dc=com',
    'gidNumber': 9999,
    'givenName': 'None',
    'homeDirectory': '/home/james',
    'loginShell': 'None',
    'mail': ['jason@mail.ru'],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount'],
    'postalCode': 344134,
    'sn': 'James',
    'sshPublicKey': ["ssh-rsa dasdffff= fsdf"],
    'st': 'None',
    'street': 'None',
    'uid': 'james',
    'uidNumber': 9999,
    'userPassword': 'asdasdasdasd'
}
data_user_post_james_data_not_ldappublickey_simple_user = {
    'cn': 'James Raf',
    'displayName': 'None',
    'dn': 'uid=james,ou=people,dc=example,dc=com',
    'gidNumber': 10003,
    'givenName': 'None',
    'homeDirectory': '/home/james',
    'loginShell': 'None',
    'mail': ['jason@mail.ru'],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount'],
    'postalCode': 344134,
    'sn': 'James',
    'sshPublicKey': ["ssh-rsa dasdffff= fsdf"],
    'st': 'None',
    'street': 'None',
    'uid': 'james',
    'uidNumber': 10003,
    'userPassword': 'asdasdasdasd'
}
data_user_post_james_data_incorrect_password_simple_user = {
    'cn': 'James Raf',
    'displayName': 'None',
    'dn': 'uid=james,ou=people,dc=example,dc=com',
    'gidNumber': 10003,
    'givenName': 'None',
    'homeDirectory': '/home/james',
    'loginShell': 'None',
    'mail': ['jason@mail.ru'],
    'objectClass': ['inetOrgPerson',
                    'posixAccount',
                    'shadowAccount',
                    'ldapPublicKey'],
    'postalCode': 344134,
    'sn': 'James',
    'sshPublicKey': ["ssh-rsa dasdffff= fsdf"],
    'st': 'None',
    'street': 'None',
    'uid': 'james',
    'uidNumber': 10003,
    'userPassword': 'asdada'
}


# Patch

data_user_patch_rambo_for_create = {
    'cn': 'Rambo Ram',
    'displayName': 'Rambo Ram',
    'dn': 'uid=rambo,ou=people,dc=example,dc=com',
    'gidNumber': 10005,
    'givenName': 'Rambo',
    'homeDirectory': '/home/rambo',
    'loginShell': '/bin/bash',
    'mail': ['rambo@mail.ru'],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount',
                 'ldapPublicKey'],
    'postalCode': 1244541,
    'sn': 'Rambo',
    'sshPublicKey': ['sdfsdf'],
    'st': 'nebraska',
    'street': 'green 1',
    'uid': 'rambo',
    'uidNumber': 10005,
    'userPassword': '12345678'
}
data_user_patch_rambo_simple_user = {
    'cn': 'Rambo Ram',
    'displayName': 'Rambo Ram',
    'gidNumber': 10006,
    'givenName': 'Rambo',
    'homeDirectory': '/home/rambo',
    'loginShell': '/bin/bash',
    'mail': ["rambo@mail.ru"],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount',
                 'ldapPublicKey'
                    ],
    'postalCode': None,
    'sn': 'Rambo',
    'sshPublicKey': ["sdfsdf"],
    'st': None,
    'street': None,
    'uid': 'rambo',
    'uidNumber': 10006
}
data_user_patch_rambo_not_webadmins_simple_user = {
    'mail': ["rambo123123@mail.ru"],
    'sshPublicKey': ["ssh-dsa sdfsdf= asdasd", "ssh-rsa 213asda4= adsasd"],
}
data_user_patch_rambo_not_webadmins_none_user_password_simple_user = {
    'mail': ["rambo123123@mail.ru"],
    'sshPublicKey': ["ssh-dsa sdfsdf= asdasd", "ssh-rsa 213asda4= adsasd"],
    'userPassword': None
}
data_user_patch_rambo_change_dn = {
    'dn': 'uid=rambo123,ou=people,dc=example,dc=com'
}

data_user_patch_john_with_none_fields = {'cn': 'john1',
    'displayName': 'John Swan',
    'gidNumber': 11022,
    'givenName': 'John Swan',
    'homeDirectory': '/home/john',
    'loginShell': '/bin/bash',
    'mail': ['john@mail.ru'],
    'objectClass': ['inetOrgPerson',
                 'posixAccount',
                 'shadowAccount',
                 'ldapPublicKey'],
    'postalCode': None,
    'sn': 'Swan22',
    'sshPublicKey': ['11112123'],
    'st': '1',
    'street': None,
    'uid': 'john',
    'uidNumber': 11022
}
data_user_patch_james_data_required_fields_simple_user = {
    'cn': 'James Raf',
    'homeDirectory': '/home/james',
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount', 'ldapPublicKey'],
    'sn': 'James',
    'uid': 'james',
    'userPassword': '12341234',

    'uidNumber': 11022,
    'street': None,
    'postalCode': None,
    'sshPublicKey': ['11112123'],
    'loginShell': '/bin/bash',
    'mail': ['james@mail.ru'],
    'gidNumber': 11022,
    'givenName': 'James NEc',
}


# Delete


# Group

# Post
data_group_post_rambo = {
    'cn': 'rambo',
    'dn': 'cn=rambo,ou=groups,dc=example,dc=com',
    'gidNumber': 10005,
    'memberUid': 'rambo',
    'objectClass': ['posixGroup']
}
data_group_post_rambo_incorrect_data = {
    'cn': 'rambodd',
    'dn': 'cn=rambo,ou=groups,dc=example,dc=com',
    'gidNumber': 10004,
    'memberUid': 'ramboasd',
    'objectClass': ['posixGroup',]
}
data_group_post_rambo_invalid_object_class = {
    'cn': 'rambo',
    'dn': 'cn=rambo,ou=groups,dc=example,dc=com',
    'gidNumber': 10005,
    'memberUid': 'rambo',
    'objectClass': ['asdasdasda']
}

# Patch
data_group_patch_rambo = {
    'cn': 'rambo',
    'gidNumber': 10006,
    'memberUid': 'rambo',
    'objectClass': ['posixGroup']
}
data_group_patch_several_member_uid = {
    'memberUid': ['rambo', 'rambo1'],
}
data_group_patch_rambo_invalid_object_class = {
    'objectClass': ['posixGroup', 'asdafaf']
}

data_group_post_rambo_for_create_without_member_uid = {
    'cn': 'rambo',
    'dn': 'cn=rambo,ou=groups,dc=example,dc=com',
    'gidNumber': 10005,
    'objectClass': ['posixGroup']
}
