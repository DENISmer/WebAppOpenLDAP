
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
        'uid': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read'],
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
            'required': []
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
            'type': TYPE_STR,
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
webadmins_fields = {
    'fields': {
        'dn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read',],
            'required': ['create',],
        },
        'uid': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['create', 'update'],
        },
        'uidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'gidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'st': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'mail': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'sshPublicKey': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'street': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'cn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'displayName': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'givenName': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'sn': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'loginShell': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'homeDirectory': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'objectClass': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update',],
            'required': ['create', 'update'],
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
            'operation': ['read', 'update',],
            'required': ['update'],
        }
    },
}

search_fields = {
    'cn': '*%s*',
    'street': '*%s*',
    'mail': '*%s*',
    'sn': '*%s*',
    'st': '*%s*',
    'givenName': '*%s*',
    'displayName': '*%s*',
    'uidNumber': '%d',
    'gidNumber': '%d',
    'postalCode': '%d',
    'loginShell': '*%s*',
    'homeDirectory': '*%s*',
    # 'objectClass': '*%s*',
}
