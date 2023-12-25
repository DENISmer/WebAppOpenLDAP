
from ldap3 import Tls, Connection, Server, SASL, ALL, ALL_ATTRIBUTES
import ssl
import pprint
import config
import orjson


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
    '(objectClass=person)',
    attributes=ALL_ATTRIBUTES
)

# True - not empty, False - empty
print('connection', connection_search)

# output data
list_users = []
if connection_search:
    print('connection entries is performed')
    list_users = connection.entries
    # for item in connection.entries:
    #     print(item['sshPublicKey'])
    # print('connection request',)
    pprint.pprint(connection.request)

connection.unbind()

import json

print('len', len(list_users))
new_users = []
for item in list_users[:4]:
    # pprint.pprint(item)
    # del item.__dict__['_state']
    # for key in item.__dict__:
    #     # print(f'\"{key}\": \"{item[key]}\"')
    #     print(f'\"{key}\":')
    # print(item["homeDirectory"])
    # print(item["sn"])

    # if item["sshPublicKey"] is list:
    # print(len(item["sshPublicKey"]), list(item["sshPublicKey"]))
    sshkey_list = []
    for sshkey in item["sshPublicKey"]:
        sshkey_list.append(str(sshkey))

    user = {
        "homeDirectory":str(item["homeDirectory"]),
        "sn":str(item["sn"]),
        "givenName":str(item["givenName"]),
        "cn":str(item["cn"]),
        "displayName":str(item["displayName"]),
        "mail":str(item["mail"]),
        "gidNumber":str(item["gidNumber"]),
        "st":str(item["st"]),
        "objectClass":str(item["objectClass"]),
        "sshPublicKey":sshkey_list,
        "street":str(item["street"]),
        "uid":str(item["uid"]),
        "postalCode":str(item["postalCode"]),
        "loginShell":str(item["loginShell"]),
        "uidNumber":str(item["uidNumber"]),
    }
    new_users.append(user)

with open('users_from_ldap.json', 'w') as f:
    json.dump(new_users, f)
# list_users_json = json.loads(list_users)
# print(list_users_json)