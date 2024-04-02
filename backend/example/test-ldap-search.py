import ldap3
import orjson
from ldap3 import Tls, Connection, Server, SASL, ALL_ATTRIBUTES, SUBTREE
import ssl
import pprint
from backend.example.config import CERT_FILE, HOSTS, TEST_USERNAME, TEST_PASSWORD

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
    '(uid=alex)',
    attributes=['jpegPhoto']
)
ssh_key = connection.entries[0]
# pprint.pprint(ssh_key)
ssh_key_json = orjson.loads(connection.entries[0].entry_to_json())
# print(ssh_key_json)
print(type(ssh_key["jpegPhoto"]), len(ssh_key["jpegPhoto"]))
print(type(ssh_key["jpegPhoto"][0]))
# print(ssh_key["jpegPhoto"][0])
import base64
# print(ssh_key["jpegPhoto"][0])
data_file = base64.b64decode(ssh_key["jpegPhoto"].value)
# for line in ssh_key["jpegPhoto"]:
#     print('++|++ ->>', line)
print(type(data_file))
# pprint.pprint(ssh_key.jpegPhoto.__dict__)
for item in ssh_key["jpegPhoto"].__dict__:
    print(item)

pprint.pprint(ssh_key.jpegPhoto.__dict__["response"])
with open('file.bin', 'wb') as fb:
    fb.write(ssh_key.jpegPhoto.value)
# pprint.pprint(ssh_key_json)
jpeg_photo = ssh_key_json["attributes"]["jpegPhoto"]
# print(type(jpeg_photo), len(jpeg_photo))
# for item in jpeg_photo[0]:
#     print(item)

print(type(jpeg_photo[0]["encoded"]), len(jpeg_photo[0]["encoded"]))
chunks = jpeg_photo[0]["encoded"].encode()
# print(ssh_key["jpegPhoto"])
# pprint.pprint(ssh_key['attributes']["jpegPhoto"])
# print(len(ssh_key['attributes']["jpegPhoto"][0]))
# chunks = b''.join(list(ssh_key['attributes']["jpegPhoto"][0]))
# chunks = ssh_key["jpegPhoto"]
exit(0)
import magic, mimetypes, base64
# print(chunks)
data_file = base64.b64decode(chunks)

format_file = magic.from_buffer(data_file, mime=True)
extension_tmp = mimetypes.guess_extension(format_file)
with open(f'image-test{extension_tmp}', 'wb') as f:
    f.write(data_file)
print(format_file, extension_tmp)


import numpy as np
from PIL import Image


# Read file using numpy "fromfile()"
# with open(f'image-test{extension_tmp}', mode='rb') as f:

Image.open(f'image-test{extension_tmp}').save('image-test.png', 'PNG')

# for key, value in ssh_key["attributes"].items():
#     print(key)
# print(type(ssh_key), bytearray(ssh_key).decode())

# True - not empty, False - empty
print('connection', connection_search)
exit(0)
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
