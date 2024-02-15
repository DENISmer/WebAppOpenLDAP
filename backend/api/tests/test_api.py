import orjson

from backend.api.tests.datatest import data_john_user


def test_get_john(client):
    response = client.get(f'/api/v1/users/{data_john_user["uid"]}')
    response_data = orjson.loads(response.data)

    assert response.status_code == 200
    assert response_data == data_john_user


def test_patch_john(client):
    data = orjson.dumps({'sshPublicKey': ['adsdasdasd']})
    headers = {'Content-Type': 'application/json'}
    response = client.patch(f'/api/v1/users/{data_john_user["uid"]}', data=data, headers=headers)

    response_data = orjson.loads(response.data)
    data = {
        'fields': {'sshPublicKey': ["attribute 'sshPublicKey' not allowed"]},
        'status': 400
    }

    assert response.status_code == 400
    assert response_data == data
