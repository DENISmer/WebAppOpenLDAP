#!/bin/bash

# Params
export LDAP_HOST=${1:-"0.0.0.0"};
export PATH_TO_LDAP_FILES=${2:-"."};


echo $LDAP_HOST;
echo $PATH_TO_LDAP_FILES;