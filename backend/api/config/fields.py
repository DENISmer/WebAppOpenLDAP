
TYPE_LIST = list
TYPE_STR = str
TYPE_INT = int

# Fields for simple user
simple_user_fields = {
    'fields': {
        'dn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'uidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['read',],
        },
        'gidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['read'],
        },
        'st': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'mail': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', 'update',],
        },
        'sshPublicKey': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', 'update'],
        },
        'userPassword': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['update', ],
        },
        'street': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'cn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'displayName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read'],
        },
        'givenName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'sn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'loginShell': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', ],
        },
        'homeDirectory': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read', ],
        },
        'objectClass': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', ],
        },
        'postalCode': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['read',],
        }
    },
}

# Fields for admin
admin_fields = {
    'fields': {
        'dn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read',],
        },
        'uidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update'],
        },
        'gidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update'],
        },
        'st': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'mail': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'sshPublicKey': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'street': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'cn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'displayName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'givenName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'sn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'loginShell': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'homeDirectory': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
        },
        'objectClass': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update',],
        },
        'userPassword': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update',],
        },
        'postalCode': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update',],
        }
    },
}

search_fields = {
    'gecos': '*%s*',
    'gidNumber': '%s',
    'givenName': '*%s*',
}
