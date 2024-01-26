import ldap3
import orjson
from ldap3 import Tls, Connection, Server, SASL, ALL_ATTRIBUTES, SUBTREE
import ssl
import pprint
from backend.tests.config import CERT_FILE, HOSTS, TEST_USERNAME, TEST_PASSWORD

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
    '(objectClass=person)',
    attributes=['gidNumber']
)


# True - not empty, False - empty
print('connection', connection_search)

# output data
list_gid_number = []
if connection_search:
    print('connection entries is performed')
    for item in connection.entries:
        json_data = orjson.loads(item.entry_to_json())
        # print(json_data['attributes'])
        list_gid_number.append(json_data['attributes']['gidNumber'][0])


def get_free_spaces(ids):
    sorted_ids = sorted(ids)
    for i in range(len(sorted_ids) - 1):
        count_free_spaces = sorted_ids[i+1] - sorted_ids[i] - 1
        if count_free_spaces > 0:
            return sorted_ids[i] + 1

# print(list_gid_number)
# print(len(list_gid_number))
# print(len(set(list_gid_number)))
sorted_list = sorted(list_gid_number)
# sorted_list.insert(0, 9990)

print(get_free_spaces(sorted_list))



# for i in range(len(sorted_list)-1):
#     # print(sorted_list[i])
#     len_free_spaces = sorted_list[i+1] - sorted_list[i] - 1
#     if len_free_spaces > 0:
#         print(len_free_spaces, '[', sorted_list[i], '-', sorted_list[i+1], ']')
#         for j in range(sorted_list[i]+1, sorted_list[i+1]):
#             print(j, end=' ')
#         print('')
    # print('\t', len_free_spaces)

connection.unbind()
exit(0)

entries = connection.extend.standard.paged_search(
    search_base='dc=local,dc=net',
    search_filter='(objectClass=person)',
    search_scope=SUBTREE,
    attributes=['cn', 'givenName'],
    paged_size=10,
    generator=False,
)

print('len entries:', len(entries))

# user_gr = connection.search(
#     'dc=local,dc=net',
#     '(cn=*admin*)',
#     attributes=ALL_ATTRIBUTES
# )
# print('user_gr', user_gr)
# for item in connection.entries:
#     print(item.entry_to_json())
# for entry in entries:
    # print(entry['attributes'])

connection.unbind()

# import json

print('len', len(list_users))
new_users = []
count = 0
# for item in list_users:
    # sshkey_list = []
    # for sshkey in item["sshPublicKey"]:
    #     sshkey_list.append(str(sshkey))
    # print(item.items())
    # if not item.__dict__.get('sshPublicKey'):
    #     count += 1
    # user = {
    #     "homeDirectory":str(item["homeDirectory"]),
    #     "sn":str(item["sn"]),
    #     "givenName":str(item["givenName"]),
    #     "cn":str(item["cn"]),
    #     "displayName":str(item["displayName"]),
    #     "mail":str(item["mail"]),
    #     "gidNumber":str(item["gidNumber"]),
    #     "st":str(item["st"]),
    #     "objectClass":str(item["objectClass"]),
    #     "sshPublicKey":sshkey_list,
    #     "street":str(item["street"]),
    #     "uid":str(item["uid"]),
    #     "postalCode":str(item["postalCode"]),
    #     "loginShell":str(item["loginShell"]),
    #     "uidNumber":str(item["uidNumber"]),
    # }
    # new_users.append(user)

# with open('users_from_ldap.json', 'w') as f:
#     json.dump(new_users, f)
# list_users_json = json.loads(list_users)
# print(list_users_json)

print(count)
