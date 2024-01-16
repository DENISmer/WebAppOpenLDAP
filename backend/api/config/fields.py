
# Fields for simple user
simple_user = {
    'fields': {
        'dn': {
            'type': 'str',
            'element_type': 'str',
            'operation': ['read',],
        },
        'uidNumber': {
            'type': 'int',
            'element_type': 'int',
            'operation': ['read',],
        },
        'gidNumber': {
            'type': 'int',
            'element_type': 'int',
            'operation': ['read'],
        },
        'st': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read',],
        },
        'mail': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read', 'update',],
        },
        'sshPublicKey': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read', 'update'],
        },
        'street': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read',],
        },
        'cn': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read',],
        },
        'displayName': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read'],
        },
        'givenName': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read',],
        },
        'sn': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read',],
        },
        'loginShell': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read', ],
        },
        'homeDirectory': {
            'type': 'str',
            'element_type': 'str',
            'operation': ['read', ],
        },
        'objectClass': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['read', ],
        },
        'userPassword': {
            'type': 'str',
            'element_type': 'str',
            'operation': ['update', ],
        },
    },
}

# Fields for admin
admin = {
    'fields': {
        'dn': {
            'type': 'str',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'uidNumber': {
            'type': 'int',
            'element_type': 'int',
            'operation': ['create', 'read', 'update'],
        },
        'gidNumber': {
            'type': 'int',
            'element_type': 'int',
            'operation': ['create', 'read', 'update'],
        },
        'st': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'mail': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'sshPublicKey': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'street': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'cn': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'displayName': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'givenName': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'sn': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'loginShell': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'homeDirectory': {
            'type': 'str',
            'element_type': 'str',
            'operation': ['create', 'read', 'update'],
        },
        'objectClass': {
            'type': 'list',
            'element_type': 'str',
            'operation': ['create', 'read', 'update',],
        },
        'userPassword': {
            'type': 'str',
            'element_type': 'str',
            'operation': ['create', 'read', 'update',],
        },
    },
}

search_fields = {
    'gecos': '*%s*',
    'gidNumber': '%s',
    'givenName': '*%s*',
}
