config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostname of your LDAP Server
config['LDAP_HOST'] = '0.0.0.0'

# Base DN of your directory
config['LDAP_BASE_DN'] = 'dc=example,dc=com'

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'ou=People'

# Groups DN to be prepended to the Base DN
# config['LDAP_GROUP_DN'] = 'ou=groups'


# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
config['LDAP_USER_LOGIN_ATTR'] = 'uid'
config['LDAP_SEARCH_FOR_GROUPS'] = False

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = None

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = None