#!/bin/bash

# Params
export LDAP_IP=${1:-"0.0.0.0"};

# Install ldap-utils
STATUS_LDAP_UTILS=`dpkg -s ldap-utils | grep Status`;

if ! [ -n "$STATUS_LDAP_UTILS" ]; then
  sudo apt install ldap-utils -y;
fi

# LDAP hosts
LDAP_HOST="ldap://$LDAP_IP:389";
LDAPI_HOST="ldap://$LDAP_IP/";

# List files
export LDAP_FILES_CONF=(modify_olcdatabase.ldif openssh-lpk_openldap.ldif ppolicy-conf.ldif);
LDAP_FILES_DATA=(add_group_webadmins.ldif add_content.ldif);
LDAP_FILES=( "$LDAP_FILES_DATA" "$LDAP_FILES_CONF" );

PATH_TO_LDAP_FILES_DOCKER=/opt/ldap/files

# Check files
for file in ${LDAP_FILES[*]}; do
  if ! [ -s $PATH_TO_LDAP_FILES_DOCKER/$file ]; then
    echo $file 'is not exist!';
    exit 1;
  fi
done

## Add conf files, executing commands
ldapadd -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/openssh-lpk_openldap.ldif;
sleep 1
ldapmodify -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/ppolicy-module.ldif;
sleep 1
ldapadd -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/ppolicy-conf.ldif;
sleep 1

# Add data files
ldapadd -H $LDAP_HOST -f $PATH_TO_LDAP_FILES_DOCKER/add_content.ldif -D cn=admin,dc=example,dc=com -w 1234;
sleep 1
ldapadd -H $LDAP_HOST -f $PATH_TO_LDAP_FILES_DOCKER/add_group_webadmins.ldif -D cn=admin,dc=example,dc=com -w 1234;
sleep 1

## Add conf files, executing commands
ldapmodify -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/modify_olcdatabase.ldif;