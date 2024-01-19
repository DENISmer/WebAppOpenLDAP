
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
            'required': [],
        },
        'uidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['read',],
            'required': [],
        },
        'gidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['read'],
            'required': [],
        },
        'st': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'mail': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', 'update',],
            'required': ['update'],
        },
        'sshPublicKey': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', 'update'],
            'required': ['update'],
        },
        'userPassword': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['update', ],
            'required': ['update']
        },
        'street': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'cn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'displayName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read'],
            'required': [],
        },
        'givenName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'sn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'loginShell': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', ],
            'required': [],
        },
        'homeDirectory': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read', ],
            'required': [],
        },
        'objectClass': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', ],
            'required': [],
        },
        'postalCode': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['read',],
            'required': [],
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
            'required': [],
        },
        'gidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'st': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'mail': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'sshPublicKey': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'street': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'cn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'displayName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'givenName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'sn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'loginShell': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'homeDirectory': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
        'objectClass': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update',],
            'required': [],
        },
        'userPassword': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update',],
            'required': [],
        },
        'postalCode': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update',],
            'required': [],
        }
    },
}

search_fields = {
    'gecos': '*%s*',
    'gidNumber': '%d',
    'givenName': '*%s*',
    'dn': '*%s*'
}
