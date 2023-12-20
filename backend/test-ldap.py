
from ldap3 import Tls, Connection, Server, SASL, ALL, ALL_ATTRIBUTES
import ssl
import pprint
import config

# LDAP connection test

# Tls
cert_file = config.CERT_FILE
tls = Tls(validate=ssl.CERT_REQUIRED, ca_certs_file=cert_file) # local_certificate_file=cert_file,  version=ssl.PROTOCOL_TLSv1_2

# Server
host = config.HOSTS[0]
server = Server(host, use_ssl=True, tls=tls)
# port=636, get_info=ALL
print(server)

# Connection
username = config.TEST_USERNAME
password = config.TEST_PASSWORD
connection = Connection(
    server,
    user=f'uid={username},ou=people,dc=local,dc=net',
    password=password,
    sasl_mechanism='EXTERNAL',
    authentication=SASL,
)
connection.open()
connection.start_tls()
connection.bind()
# pprint.pprint(connection.__dict__)
connection_search = connection.search(
    'dc=local,dc=net',
    '(uid=serbinovichgs)',
    attributes=ALL_ATTRIBUTES
)

# True - not empty, False - empty
print('connection', connection_search)

# output data
if connection_search:
    print('connection entries', 'connection.entries')
    for item in connection.entries:
        print(item['sshPublicKey'])
    print('connection request',)
    pprint.pprint(connection.request)

connection.unbind()