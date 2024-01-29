

olcAccess to change:

    olcAccess: to attrs=userPassword
      by self write
      by group.exact="cn=webadmins,ou=Groups,dc=example,dc=com" write
      by anonymous auth
      by * none
    
    olcAccess: to *
      by self write
      by group.exact="cn=webadmins,ou=Groups,dc=example,dc=com" write
      by * read

## OpenLDAP

-----
OpenLDAP [Documentation](https://help.ubuntu.ru/wiki/%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE_%D0%BF%D0%BE_ubuntu_server/%D0%B0%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%BF%D0%BE_%D1%81%D0%B5%D1%82%D0%B8/openldap_server#tls)

Install OpenLDAP:

    sudo apt-get install slapd ldap-utils

Reconfiguration OpenLDAP:

    sudo dpkg-reconfigure slapd

Input domain name - example, organization name - com;

Add some content such as groups, users:

    ldapadd -H ldap:/// -f add_conntent.ldif -D cn=admin,dc=example,dc=com -W

Add webadmins group:

    ldapadd -H ldap:/// -f add_group_webadmins.ldif -D cn=admin,dc=example,dc=com -W

Modify olcDatabase:
    
    ldapmodify -H ldap:/// -f modify_olcdatabase.ldif -D cn=admin,dc=example,dc=com -W



## Flask

-----
Install required packages:

    pip install -r requirements.txt

Run app:

    flask --app application run --reload