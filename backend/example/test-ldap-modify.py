import pprint
import time

import ldap3

server = ldap3.Server('192.168.1.12', 389)

connection = ldap3.Connection(
    server,
    user='uid=bob,ou=People,dc=example,dc=com',
    password='bob',
    sasl_mechanism='EXTERNAL',
    # authentication=ldap3.SASL,
)
connection.open()
connection.bind()

connection_search = connection.search('dc=example,dc=com', '(uid=bob)', attributes=ldap3.ALL_ATTRIBUTES)
print('Connection search:', connection_search)
if connection_search:
    pprint.pprint(connection.response[0])

time.sleep(1)
print('End sleep')

connection_modify = connection.modify('uid=bob,ou=People,dc=example,dc=com', {
    'sn': [(ldap3.MODIFY_REPLACE, ['Doe1'])]
})
print('connection modify', connection_modify)
print('Connection result', connection.result)

time.sleep(1)
print('End sleep')
connection.unbind()

connection_search = connection.search('dc=example,dc=com', '(uid=bob)', attributes=ldap3.ALL_ATTRIBUTES)
print('Connection search:', connection_search)
if connection_search:
    pprint.pprint(connection.response[0])


connection.unbind()
