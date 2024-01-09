simple_user = {
    'fields': {
        'update': [
            'mail', 'sshPublicKey', 'userPassword',
        ],
        'read': [
            'dn', 'uidNumber', 'gidNumber', 'st', 'mail', 'street', 'cn', 'displayName', 'givenName', 'sn',
        ]
    },
}

admin = {
    'fields': {
        'update': [
            'uidNumber', 'gidNumber', 'st', 'mail', 'street', 'cn', 'displayName', 'givenName', 'sn',
        ],
        'read': [
            'dn', 'uidNumber', 'gidNumber', 'st', 'mail', 'street', 'cn', 'displayName', 'givenName', 'sn',
        ]
    },
}
