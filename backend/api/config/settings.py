import os
from dotenv import load_dotenv

load_dotenv()

# Config app
SECRET_KEY = 'secret'
DEBUG = True
ALGORITHMS = 'HS256'

# Config LDAP
# Hostname of your LDAP Server
LDAP_HOST = '0.0.0.0'

# Base DN of your directory
LDAP_BASE_DN = 'dc=example,dc=com'

# Users DN to be prepended to the Base DN
LDAP_USER_DN = 'ou=People'

# Groups DN to be prepended to the Base DN
# config['LDAP_GROUP_DN'] = 'ou=groups'

# The RDN attribute for your user schema on LDAP
LDAP_USER_RDN_ATTR = 'cn'

# The Attribute you want users to authenticate to LDAP with.
LDAP_USER_LOGIN_ATTR = 'uid'
LDAP_SEARCH_FOR_GROUPS = False

# The Username to bind to LDAP with
LDAP_BIND_USER_DN = None

# The Password to bind to LDAP with
LDAP_BIND_USER_PASSWORD = None

