
# Fields for simple user
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

# Fields for admin
admin = {
    'fields': {
        'update': [
            'uidNumber', 'gidNumber', 'st', 'mail', 'street', 'cn', 'displayName', 'givenName', 'sn',
        ],
        'read': [
            'dn', 'uidNumber', 'gidNumber', 'st', 'mail', 'street',
            'cn', 'displayName', 'givenName', 'sn', 'objectClass',
        ]
    },
}

search_fields = {
    'gecos': '*%s*',
    'gidNumber': '%s',
    'givenName': '*%s*',
}
