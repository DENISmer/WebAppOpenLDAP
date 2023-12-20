import ldap3

server = ldap3.Server('0.0.0.0')

connection = ldap3.Connection(
    server,
    user='uid=bob,ou=People,dc=example,dc=com',
    password='bob',
    sasl_mechanism='EXTERNAL',
    authentication=ldap3.SASL,
)
connection.open()
connection.bind()

connection_search = connection.search('dc=example,dc=com', '(uid=bob)', attributes=ldap3.ALL_ATTRIBUTES)
print('Connection search:', connection_search)
if connection_search:
    print(connection.entries)

connection_modify = connection.modify('uid=bob,ou=People,dc=example,dc=com', {
    'sn': [(ldap3.MODIFY_REPLACE, ['Doe1'])]
})
print('Connection result', connection.result)

connection.unbind()
