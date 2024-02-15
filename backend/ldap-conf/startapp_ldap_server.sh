#!/bin/bash

# Params
export LDAP_IP=${1:-"0.0.0.0"};
export PATH_TO_LDAP_FILES=${2:-"."};

# Install ldap-utils
STATUS_LDAP_UTILS=`dpkg -s ldap-utils | grep Status`;

if ! [ -n "$STATUS_LDAP_UTILS" ]; then
  sudo apt install ldap-utils -y;
fi

# LDAP hosts
LDAP_HOST="ldap://$LDAP_IP:8389";
LDAPI_HOST="ldapi:///";

# List files
LDAP_FILES_CONF=(modify_olcdatabase.ldif openssh-lpk_openldap.ldif ppolicy-conf.ldif);
LDAP_FILES_DATA=(add_group_webadmins.ldif add_content.ldif);
LDAP_FILES=( "$LDAP_FILES_DATA" "$LDAP_FILES_CONF" );

# Check files
for file in ${LDAP_FILES[*]}; do
  if ! [ -s $PATH_TO_LDAP_FILES/$file ]; then
    echo $file 'is not exist!';
    exit 1;
  fi
done

# Params docker
DOCKER_TAG_IMAGE=ldap-server
DOCKER_NAME_CONTAINER=ldap-name-server
PATH_TO_LDAP_FILES_DOCKER=/opt/ldap/files

# Building docker image
sudo docker build -f backend/ldap-conf/Dockerfile -t $DOCKER_TAG_IMAGE .

# Run docker container
sudo docker run --name $DOCKER_NAME_CONTAINER -p 0.0.0.0:8389:389 --rm -d $DOCKER_TAG_IMAGE
sleep 2
#sudo docker exec ldap-name-server ldapsearch -Q -Y EXTERNAL -H ldapi:/// -b cn=config -LLL '(olcDatabase={1}mdb)'

## Add conf files, executing commands
sudo docker exec $DOCKER_NAME_CONTAINER ldapadd -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/openssh-lpk_openldap.ldif;
sudo docker exec $DOCKER_NAME_CONTAINER ldapmodify -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/ppolicy-module.ldif;
sudo docker exec $DOCKER_NAME_CONTAINER ldapadd -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/ppolicy-conf.ldif;

# Add data files

ldapadd -H $LDAP_HOST -f $PATH_TO_LDAP_FILES/add_content.ldif -D cn=admin,dc=example,dc=com -w 1234;
ldapadd -H $LDAP_HOST -f $PATH_TO_LDAP_FILES/add_group_webadmins.ldif -D cn=admin,dc=example,dc=com -w 1234;

## Add conf files, executing commands
sudo docker exec $DOCKER_NAME_CONTAINER ldapmodify -Q -Y EXTERNAL -H $LDAPI_HOST -f $PATH_TO_LDAP_FILES_DOCKER/modify_olcdatabase.ldif;