FROM osixia/openldap:latest

ENV LDAP_ORGANISATION=People
ENV LDAP_ADMIN_PASSWORD=1234
ENV LDAP_DOMAIN=example.com

COPY ../../backend/ldap/openssh-lpk_openldap.schema /etc/ldap/schema/openssh-lpk_openldap.schema
COPY ../../backend/ldap/openssh-lpk_openldap.ldif /opt/ldap/files/openssh-lpk_openldap.ldif
COPY ../../backend/ldap/ppolicy-conf.ldif /opt/ldap/files/ppolicy-conf.ldif
COPY ../../backend/ldap/ppolicy-module.ldif /opt/ldap/files/ppolicy-module.ldif
COPY ../../backend/ldap/modify_olcdatabase.ldif /opt/ldap/files/modify_olcdatabase.ldif