import os
from dotenv import load_dotenv


load_dotenv()
config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostnames of your LDAP Servers
config['LDAP_HOSTS'] = os.getenv('LDAP_HOSTS').split(',')

# Port of your LDAP Servers
config['LDAP_PORT'] = int(os.getenv('LDAP_PORT'))

# Base DN of your directory
config['LDAP_BASE_DN'] = 'dc=example,dc=com'

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'ou=People'

# Groups DN to be prepended to the Base DN
# config['LDAP_GROUP_DN'] = 'ou=groups'

config['LDAP_READONLY'] = False

# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
config['LDAP_USER_LOGIN_ATTR'] = 'uid'
config['LDAP_SEARCH_FOR_GROUPS'] = False

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = None

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = None

# The SSL to use the crypt data
config['LDAP_USE_SSL'] = False

# The path to certificate
config['CERT_PATH'] = os.getenv('CERT_PATH')

# Instruct Flask-LDAP3-Login to not automatically add the server
config['LDAP_ADD_SERVER'] = False