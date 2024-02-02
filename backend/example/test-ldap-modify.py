import ldap3

server = ldap3.Server('0.0.0.0')

connection = ldap3.Connection(
    server,
    user='uid=bob,ou=People,dc=example,dc=com',
    password='bob',
    sasl_mechanism='EXTERNAL',
    # authentication=ldap3.SASL,
)
connection.open()
connection.bind()

print(connection.result)
connection_search = connection.search('dc=example,dc=com', '(uid=bob)', attributes=ldap3.ALL_ATTRIBUTES)
print('Connection search:', connection_search)
if connection_search:
    print(connection.entries)

# connection_modify = connection.modify('uid=bob,ou=People,dc=example,dc=com', {
#     'sn': [(ldap3.MODIFY_REPLACE, ['Doe1'])]
# })
# print('Connection result', connection.result)


# from ldap3 import set_config_parameter, get_config_parameter
#
# set_config_parameter('ATTRIBUTES_EXCLUDED_FROM_CHECK', get_config_parameter('ATTRIBUTES_EXCLUDED_FROM_CHECK') + ['-'])


print('DELETE ATTRS TOM3') # SOLUTION for delete!!!!
connection.modify('uid=tom3,ou=People,dc=example,dc=com',{
    'sshPublicKey': [(ldap3.MODIFY_REPLACE, [b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDMjpdD7QfLtcv5sEJnuG9SEJeTyOqzCfhiMHRb1hfeefAPAeV9on3nrNiCQ6o+S/vKgHTIk0gjV3Q/j68pH793BeDXrnNo9oeViq2XCP3PQDeaf8hQqVRMP4qazCzOG47KJn9yNZRMf8+hI7Xg2D3OnIyanFpKO2ICam8oEbfWYKMrKM7hlywNgemrnaLqZzcMC7YWMQS1Ro573lRPWrZoakKT/7phcG60Vi5xFg9v+/DXSX1LdsOJ1zFo3lMldzJDVTgN+l7PgqfKi4WcNKhIgeUnL7fQSl33/L435ANMHm8jf9cV01+mANSUfpZslnOTnJYeaSiK/Z9m2m3UzNRPPlXFecVFNEBNR9zx4/6JxNyQvbhcRIkzJEYoleM6CWwwxTxwqWjVRQfhZbYCLwop5gYv3v2/DKUsldPb95UBjBKHC/NmPYSAT2ZHj12IVeyMRaCwcDh8vpAB7UthIAQx/FqvOzGZArP2xOfgVWIcJ+icT22IbJ3ZsFBA8SGUBaM= grig@g-pc'])]
})
print('Connection result', connection.result)
connection.unbind()

# from ldap3 import get_config_parameter
# print(get_config_parameter('ATTRIBUTES_EXCLUDED_FROM_CHECK') + ['-'])

