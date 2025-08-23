FROM osixia/openldap:latest

#ENV LDAP_ORGANISATION=People
#ENV LDAP_ADMIN_PASSWORD=1234
#ENV LDAP_DOMAIN=example.com

COPY openssh-lpk_openldap.schema /etc/ldap/schema/openssh-lpk_openldap.schema
COPY openssh-lpk_openldap.ldif /opt/ldap/files/openssh-lpk_openldap.ldif
COPY ppolicy-conf.ldif /opt/ldap/files/ppolicy-conf.ldif
COPY ppolicy-module.ldif /opt/ldap/files/ppolicy-module.ldif
COPY modify_olcdatabase.ldif /opt/ldap/files/modify_olcdatabase.ldif
COPY add_content.ldif /opt/ldap/files/add_content.ldif
COPY add_group_webadmins.ldif /opt/ldap/files/add_group_webadmins.ldif
