

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

Input domain name - example.com, organization name - People;

Add some content such as groups, users:

    ldapadd -H ldap:/// -f add_conntent.ldif -D cn=admin,dc=example,dc=com -W

Add webadmins group:

    ldapadd -H ldap:/// -f add_group_webadmins.ldif -D cn=admin,dc=example,dc=com -W

Modify olcDatabase:
    
    sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f modify_olcdatabase.ldif -D cn=admin,dc=example,dc=com -W



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
- /api/v1/groups/{type_group}
- /api/v1/groups/{type_group}/{username_cn}


- /api/v1/users/
- /api/v1/users/me/
- /api/v1/users/{username_uid}


- /api/v1/auth/token

## Requests groups

-----
### GET LIST
**route**: /api/v1/groups/posixgroup
**GET PARAMS**: search 
```json
{
    "groups": [
        {
            "dn": "cn=testuser,ou=Groups,dc=example,dc=com",
            "gidNumber": 10000,
            "cn": "testuser",
            "objectClass": ["posixGroup"],
            "memberUid": "testuser"
        }
    ]
}
```
**status code**: 200

### GET
**route**: /api/v1/groups/posixgroup/testuser
```json
{
    "dn": "cn=testuser,ou=Groups,dc=example,dc=com",
    "gidNumber": 10000,
    "cn": "testuser",
    "objectClass": ["posixGroup"],
    "memberUid": "testuser"
}
```
**status code**: 200
### POST
**route**: /api/v1/groups/posixgroup
```json
{
    "dn": required,
    "gidNumber": required,
    "cn": required,
    "objectClass": [required],
    "memberUid": required
}
```
**status code**: 201
### PATCH
**route**: /api/v1/groups/posixgroup/testuser
```json
{
    "gidNumber": nonrequired,
    "cn": nonrequired,
    "objectClass": [nonrequired],
    "memberUid": nonrequired
}
```
**status code**: 200
### PUT
**route**: /api/v1/groups/posixgroup/testuser
- **role**: webadmins
  ```json
  {
      "gidNumber": required,
      "cn": required,
      "objectClass": [required],
      "memberUid": required
  }
  ```
**status code**: 200
### DELETE
**route**: /api/v1/groups/posixgroup/testuser
- **role**: webadmins

**status code**: 204

## Requests users

-----
### GET LIST

**GET PARAMS**: search 

**route**: /api/v1/users
```json
{
  "users":[ 
      {
        "uidNumber": 10000, 
        "gidNumber": 10000, 
        "uid": "testuser", 
        "sshPublicKey": [], 
        "st": "Moskow city", 
        "mail": ["testuser@mail.ru", "testuser@mail.ru"], 
        "street": "green street 12", 
        "cn": "Test User", 
        "displayName": "Test User", 
        "givenName": "testuser", 
        "sn": "Test User", 
        "postalCode": 123414,
        "homeDirectory": "/home/testuser", 
        "loginShell": ["/bin/bash"], 
        "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"]
      }
  ] 
}
```
### GET
**route**: /api/v1/users/testuser
```json
{
    "uidNumber": 10000, 
    "gidNumber": 10000, 
    "uid": "testuser", 
    "sshPublicKey": [], 
    "st": "Moskow city", 
    "mail": ["testuser@mail.ru", "testuser@mail.ru"], 
    "street": "green street 12", 
    "cn": "Test User", 
    "displayName": "Test User", 
    "givenName": "testuser", 
    "sn": "Test User", 
    "postalCode": 100128,
    "homeDirectory": "/home/testuser", 
    "loginShell": ["/bin/bash"], 
    "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"]
}
```
**status code**: 200
### GET
**route**: /api/v1/users/me/

**role**: webadmins

**role**: user
```json
{
    "uidNumber": 10000, 
    "gidNumber": 10000, 
    "uid": "testuser", 
    "sshPublicKey": [], 
    "st": "Moskow city", 
    "mail": ["testuser@mail.ru", "testuser@mail.ru"], 
    "street": "green street 12", 
    "cn": "testuser", 
    "displayName": "Test User", 
    "givenName": "testuser", 
    "sn": "Test User", 
    "postalCode": 100123,
    "homeDirectory": "/home/testuser", 
    "loginShell": ["/bin/bash"], 
    "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"]
}
```
**status code**: 200
### POST
**route**: /api/v1/users

**role**: webadmins
```json
{
    "dn": required
    "uidNumber": nonrequired, 
    "gidNumber": nonrequired, 
    "uid": required, 
    "sshPublicKey": [nonrequired], 
    "st": nonrequired, 
    "mail": [nonrequired], 
    "street": nonrequired, 
    "cn": required, 
    "displayName": nonrequired, 
    "givenName": nonrequired, 
    "sn": required, 
    "postalCode": nonrequired,
    "homeDirectory": required, 
    "loginShell": [nonrequired], 
    "objectClass": [required],
    "userPassword": required
}
```
**status code**: 201
### PUT
**route**: /api/v1/users/testuser
- **role**: webadmins
    ```json
    {
        "uidNumber": required, 
        "gidNumber": required, 
        "uid": required, 
        "sshPublicKey": [required], 
        "st": required, 
        "mail": [required], 
        "street": required, 
        "cn": required, 
        "displayName": required, 
        "givenName": required, 
        "sn": required, 
        "postalCode": required,
        "homeDirectory": required, 
        "loginShell": [required], 
        "objectClass": [required],
        "userPassword": required
    }
    ```
- **role**: user
    ```json
    {
        "sshPublicKey": [required], 
        "mail": [required], 
        "userPassword": [required]
    }
    ```
**status code**: 200
### PATCH
**route**: /api/v1/users/testuser
- **role**: webadmins
    ```json
    {
        "dn": nonrequired
        "uidNumber": nonrequired, 
        "gidNumber": nonrequired, 
        "uid": nonrequired, 
        "sshPublicKey": [nonrequired], 
        "st": nonrequired, 
        "mail": [nonrequired], 
        "street": nonrequired, 
        "cn": nonrequired, 
        "displayName": nonrequired, 
        "givenName": nonrequired, 
        "sn": nonrequired, 
        "postalCode": nonrequired,
        "homeDirectory": nonrequired, 
        "loginShell": [nonrequired], 
        "objectClass": [nonrequired],
        "userPassword": nonrequired
    }
    ```
- **role**: user
    ```json
    {
        "sshPublicKey": [nonrequired], 
        "mail": [nonrequired], 
        "userPassword": nonrequired
    }
    ```
**status code**: 200
### DELETE
**route**: /api/v1/users/testuser
- **role**: webadmins

**status code**: 204


## Requests tokens

-----
### POST
**route**: /api/v1/auth/token
```json
{
    "username": required,
    "userPassword": required
}
```
Response:
```json
{
    "token": "adsdasdasfasdfsdgfasdsgdsdgsd",
    "uid": "testuser"
}
```
**status code**: 200

## Docker run

