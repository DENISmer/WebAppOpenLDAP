
TYPE_LIST = list
TYPE_STR = str
TYPE_INT = int
TYPE_BYTES = bytes

# Fields for simple user
simple_user_fields = {
    'name': 'simple_user_fields',
    'fields': {
        'dn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'uid': {
            'type': TYPE_STR,
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
            'type': TYPE_STR,
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
            'required': ['create'] # create - to update for put, patch requests
        },
        'street': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'cn': {
            'type': TYPE_STR,
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
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'sn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['read',],
            'required': [],
        },
        'loginShell': {
            'type': TYPE_STR,
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
            'operation': ['read', ],
            'required': [],
        },
        'jpegPhoto': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', ],
            'required': [],
        }
    },
}

# Fields for admin
webadmins_fields = {
    'name': 'webadmins_fields',
    'fields': {
        'dn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read',],
            'required': ['create'],
        },
        'uid': {
            'type': TYPE_STR,
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
            'type': TYPE_STR,
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
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'cn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['create', 'update'],
        },
        'displayName': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'givenName': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'sn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['create', 'update'],
        },
        'loginShell': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['update'],
        },
        'homeDirectory': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['create', 'update'],
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
            'operation': ['create', 'update',],
            'required': ['create'],
        },
        'postalCode': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update',],
            'required': ['update'],
        },
        'jpegPhoto': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['read', ],
            'required': [],
        }
    },
}

files_webadmins_fields = {
    'name': 'files_webadmins_fields',
    'fields': {
        'jpegPhoto': {
            'type': TYPE_STR,
            'element_type': TYPE_BYTES,
            'operation': ['read', 'update'],
            'required': [],
        }
    }
}

webadmins_cn_posixgroup_fields = {
    'name': 'webadmins_cn_posixgroup_fields',
    'fields': {
        'dn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read',],
            'required': ['create'],
        },
        'gidNumber': {
            'type': TYPE_INT,
            'element_type': TYPE_INT,
            'operation': ['create', 'read', 'update'],
            'required': ['create', 'update'],
        },
        'objectClass': {
            'type': TYPE_LIST,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update',],
            'required': ['create', 'update'],
        },
        'cn': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': ['create', 'update'],
        },
        'memberUid': {
            'type': TYPE_STR,
            'element_type': TYPE_STR,
            'operation': ['create', 'read', 'update'],
            'required': [],
        },
    }
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


search_posixgroup_fields = {
    'cn': '*%s*',
    'memberUid': '*%s*',
    'gidNumber': '%d',
}
