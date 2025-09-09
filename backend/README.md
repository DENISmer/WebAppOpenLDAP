

## OpenLDAP

-----
OpenLDAP [Documentation](https://help.ubuntu.ru/wiki/%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE_%D0%BF%D0%BE_ubuntu_server/%D0%B0%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%BF%D0%BE_%D1%81%D0%B5%D1%82%D0%B8/openldap_server#tls)

Install OpenLDAP:

    sudo apt-get install slapd ldap-utils

Reconfiguration OpenLDAP:

    sudo dpkg-reconfigure slapd

Input domain name - example.com, organization name - People;

Add some content such as groups, users:

    ldapadd -H ldap:/// -f add_conntent.ldif -D cn=admin,dc=example,dc=com -W

Add webadmins group:

    ldapadd -H ldap:/// -f add_group_webadmins.ldif -D cn=admin,dc=example,dc=com -W

Modify olcDatabase:
    
    sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f modify_olcdatabase.ldif -D cn=admin,dc=example,dc=com -W

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

## Flask

-----
Install python environments:  

    python -m venv venv

Activate venv:

    source venv/bin/activate

Install required packages:

    pip install -r requirements.txt

Add to the .env file:

    export LDAP_HOSTS = 192.168.1.12
    export LDAP_PORT = 389
    export CERT_PATH = ///

Run app:

    flask --app application run --reload

## Gunicorn

----
Run gunicorn (example):

    gunicorn --workers 6 --bind 0.0.0.0:8080 backend.api.app:app

## Celery

-----
First, install and start redis server.

Go to root directory of the app:

    cd WebAppOpenLDAP/

Run celery (example):

    celery -A backend.api.app.celery_app worker --beat --loglevel=debug --concurrency=4


## Routes

-----
- /api/v1/groups
- /api/v1/groups
- /api/v1/groups/{username_cn}


- /api/v1/users
- /api/v1/users
- /api/v1/users/{username_uid}


- /api/v1/auth/token


##  Documentation

----
- /docs/swagger/

## Docker run

Environment files: copy "docker.env" to root app and copy ".env" to ./backend/. 

Docker build
    
    docker-compose --file docker-compose-debug.yml --env-file docker.env up

## Docker LDAP

----
Perform commands below

    docker exec -it ldap-server-container ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f /opt/ldap/files/ppolicy-module.ldif;

    docker exec -it ldap-server-container ldapadd -Q -Y EXTERNAL -H ldapi:/// -f /opt/ldap/files/ppolicy-conf.ldif;

    docker exec -it ldap-server-container ldapadd -H ldap:/// -f /opt/ldap/files/add_content.ldif -D cn=admin,dc=example,dc=com -w 1234;
    
    docker exec -it ldap-server-container ldapadd -H ldap:/// -f /opt/ldap/files/add_group_webadmins.ldif -D cn=admin,dc=example,dc=com -w 1234;
    
    docker exec -it ldap-server-container ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f /opt/ldap/files/modify_olcdatabase.ldif;