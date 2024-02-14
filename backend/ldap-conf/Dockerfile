FROM osixia/openldap:latest

ENV LDAP_ORGANISATION=People
ENV LDAP_ADMIN_PASSWORD=1234
ENV LDAP_DOMAIN=example.com

COPY ../../backend/ldap-conf/openssh-lpk_openldap.schema /etc/ldap/schema/openssh-lpk_openldap.schema
