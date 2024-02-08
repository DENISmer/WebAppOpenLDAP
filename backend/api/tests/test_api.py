import pprint

import orjson

uid = 'testuser_100'
john_user = {
    'cn': 'testuser_100',
    'displayName': 'Test User 100',
    'dn': 'uid=testuser_100,ou=People,dc=example,dc=com',
    'gidNumber': 10100,
    'givenName': 'testuser 100',
    'homeDirectory': '/home/testuser_100',
    'loginShell': ['/'],
    'mail': ['testuser_100@mail.ru', 'testuser_1002@mail.ru'],
    'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount'],
    'postalCode': None,
    'sn': 'Test User 100',
    'sshPublicKey': [],
    'st': 'Moskow city',
    'street': 'green street 12',
    'uid': 'testuser_100',
    'uidNumber': 10100
}


def test_get_john(client):
    response = client.get(f'/api/v1/users/{uid}')
    response_data = orjson.loads(response.data)

    assert response.status_code == 200
    assert response_data == john_user


def test_patch_john(client):
    data = orjson.dumps({'sshPublicKey': ['adsdasdasd']})
    headers = {'Content-Type': 'application/json'}
    response = client.patch(f'/api/v1/users/{uid}', data=data, headers=headers)

    response_data = orjson.loads(response.data)
    data = {
        'fields': {'sshPublicKey': ["attribute 'sshPublicKey' not allowed"]},
        'status': 400
    }

    assert response.status_code == 400
    assert response_data == data
