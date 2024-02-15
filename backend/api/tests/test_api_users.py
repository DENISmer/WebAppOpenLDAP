import pprint

import orjson

from backend.api.tests import datatest as dt


def authorize_user(client, user_data):
    data = orjson.dumps(user_data)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )
    response_data = orjson.loads(response.data)

    return response_data


def test_get_user_200(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_bob_webadmins["uid"]}',
        headers=headers
    )

    assert response.status_code == 200

    response_data = orjson.loads(response.data)
    expected_data = dt.data_user_get_bob_webadmins

    assert response_data == expected_data


def test_get_user_not_found_404(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_not_found["uid"]}',
        headers=headers
    )

    assert response.status_code == 404

    response_data = orjson.loads(response.data)
    expected_data = {
        'message': 'User not found',
        'status': 404
    }
    assert response_data == expected_data


def test_get_user_not_webadmins_not_own_profile_403(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_simple_user)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_bob_webadmins["uid"]}',
        headers=headers
    )

    assert response.status_code == 403

    response_data = orjson.loads(response.data)
    expected_data = {
        'message': 'Insufficient access rights',
        'status': 403
    }
    assert response_data == expected_data


def test_get_user_invalid_token_401(client):
    headers = {'Authorization': 'Bearer sfdsddfgdffsdf'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_bob_webadmins["uid"]}',
        headers=headers
    )

    assert response.status_code == 401

    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Unauthorized Access', 'status': 401}

    assert response_data == expected_data


def test_get_user_not_webadmins_own_profile_200(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_simple_user)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_john_simple_user["uid"]}',
        headers=headers
    )

    assert response.status_code == 200

    response_data = orjson.loads(response.data)
    expected_data = dt.data_user_get_john_simple_user

    assert response_data == expected_data




# def test_patch_john(client):
#     data = orjson.dumps({'sshPublicKey': ['adsdasdasd']})
#     headers = {'Content-Type': 'application/json'}
#     response = client.patch(f'/api/v1/users/{data_john_user["uid"]}', data=data, headers=headers)
#
#     response_data = orjson.loads(response.data)
#     expected_data = {
#         'fields': {'sshPublicKey': ["attribute 'sshPublicKey' not allowed"]},
#         'status': 400
#     }
#
#     assert response.status_code == 400
#     assert response_data == expected_data
