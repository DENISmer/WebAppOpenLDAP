FROM ubuntu:20.04

RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt install ldap-utils -y\
  && rm -rf /var/lib/apt/lists/*

COPY ../../../backend/ldap/openssh-lpk_openldap.ldif /opt/ldap/files/openssh-lpk_openldap.ldif
COPY ../../../backend/ldap/ppolicy-conf.ldif /opt/ldap/files/ppolicy-conf.ldif
COPY ../../../backend/ldap/ppolicy-module.ldif /opt/ldap/files/ppolicy-module.ldif
COPY ../../../backend/ldap/modify_olcdatabase.ldif /opt/ldap/files/modify_olcdatabase.ldif
COPY ../../../backend/ldap/add_content.ldif /opt/ldap/files/add_content.ldif
COPY ../../../backend/ldap/add_group_webadmins.ldif /opt/ldap/files/add_group_webadmins.ldif

COPY ../../../backend/ldap/ldap-load-data-conf/load_data_ldap_docker.sh /opt/ldap/files/load_data_ldap_docker.sh

RUN chmod u+x /opt/ldap/files/load_data_ldap_docker.sh

CMD ./opt/ldap/files/load_data_ldap_docker.sh $LDAP_HOST