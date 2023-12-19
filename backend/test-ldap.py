
from ldap3 import Tls, Connection, Server, SASL, ALL
import ssl
import pprint
import config

# LDAP connection test

# Tls
cert_file = config.CERT_FILE
tls = Tls(local_certificate_file=cert_file, validate=ssl.CERT_REQUIRED)

# Server
host = config.HOSTS[0]
server = Server(host,  get_info=ALL)
# use_ssl=True, tls=tls, port=636,
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
print(server)
# connection.start_tls()
# connection.bind()
# pprint.pprint(connection.__dict__)
connection_search = connection.search('dc=local,dc=net', '(objectclass=*)')

# True - not empty, False - empty
print('connection', connection_search)

# output data
if connection_search:
    print('connection entries', len(connection.entries))
