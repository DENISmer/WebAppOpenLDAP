import os
# from dotenv import load_dotenv
from backend.api.config import settings

# load_dotenv()
config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostnames of your LDAP Servers
config['LDAP_HOSTS'] = settings.HOSTS

# Port of your LDAP Servers
config['LDAP_PORT'] = settings.LDAP_PORT

# Base DN of your directory
config['LDAP_BASE_DN'] = 'dc=example,dc=com'

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'ou=People'

# Groups DN to be prepended to the Base DN
config['LDAP_GROUP_DN'] = 'ou=groups'

# Only read data form LDAP without write
config['LDAP_READONLY'] = False

# config['LDAP_BIND_AUTHENTICATION_TYPE'] = 'SASL'

# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
config['LDAP_USER_LOGIN_ATTR'] = 'uid'

# Specifies whether or not groups should be searched for when getting user details
config['LDAP_SEARCH_FOR_GROUPS'] = False

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = None

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = None

# The SSL to use the crypt data
config['LDAP_USE_SSL'] = settings.LDAP_USE_SSL

# The path to certificate
config['CERT_PATH'] = settings.CERT_FILE_LDAP

# Instruct Flask-LDAP3-Login to not automatically add the server
config['LDAP_ADD_SERVER'] = False

# The group object to filter
config['LDAP_GROUP_OBJECT_FILTER'] = '(objectClass=groupOfNames)'

# Specifies the LDAP attribute where group members are declared.
config['LDAP_GROUP_MEMBERS_ATTR'] = 'member'

# Check names
config['LDAP_CHECK_NAMES'] = True