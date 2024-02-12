
from ldap3 import Tls, Connection, Server, SASL, ALL_ATTRIBUTES
import ssl
import pprint
from backend.example.config import CERT_FILE, HOSTS, TEST_PASSWORD, TEST_USERNAME

# LDAP connection test

# Tls
cert_file = CERT_FILE
tls = Tls(validate=ssl.CERT_REQUIRED, ca_certs_file=cert_file) # local_certificate_file=cert_file,  version=ssl.PROTOCOL_TLSv1_2

# Server
host = HOSTS[0]
server = Server(host, use_ssl=True, tls=tls)
# port=636, get_info=ALL
print(server)

# Connection
username = TEST_USERNAME
password = TEST_PASSWORD
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
    '(objectClass=person)', #'(uid=serbinovichgs)',
    attributes=ALL_ATTRIBUTES
)

# True - not empty, False - empty
print('connection', connection_search)

# output data
if connection_search:
    pprint.pprint(connection.entries)
    # print('connection entries', 'connection.entries')
    # for item in connection.entries:
    #     print(item['sshPublicKey'])
    # print('connection request',)
    # pprint.pprint(connection.request)

connection.unbind()