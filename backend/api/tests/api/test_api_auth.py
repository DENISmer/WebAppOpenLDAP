import orjson

from backend.api.tests.api import datatest as dt


def test_auth_post_200(client):
    data = orjson.dumps(dt.data_user_auth_bob_webadmins)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )

    assert response.status_code == 200

    response_data = orjson.loads(response.data)
    expected_data = {
        'token': 'token',
        'uid': dt.data_user_auth_bob_webadmins['username'],
        'role': 'webadmins'
    }

    assert response_data.get('token') is not None

    response_data['token'] = expected_data['token']

    assert response_data == expected_data


def test_auth_invalid_data_401(client):
    data = orjson.dumps(dt.data_user_auth_bob_invalid_data)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )

    assert response.status_code == 401

    response_data = orjson.loads(response.data)
    expected_data = {
        'message': 'Invalid username or password',
        'status': 401
    }

    assert response_data == expected_data


def test_auth_more_field_400(client):
    data = orjson.dumps(dt.data_user_auth_more_field)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'gesoc': ['Unknown field.'], 'password': ['Unknown field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_auth_empty_field_400(client):
    data = orjson.dumps(dt.data_user_auth_empty_field)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'userPassword': ['Missing data for required field.'],
                   'username': ['Missing data for required field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_auth_missing_field_400(client):
    data = orjson.dumps(dt.data_user_auth_missing_field)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'userPassword': ['Missing data for required field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_auth_post_not_webadmins_200(client):
    data = orjson.dumps(dt.data_user_auth_john_simple_user)
    headers = {'Content-Type': 'application/json'}
    response = client.post(
        dt.Route.AUTH.value,
        headers=headers,
        data=data,
    )

    assert response.status_code == 200

    response_data = orjson.loads(response.data)
    expected_data = {
        'token': 'token',
        'uid': dt.data_user_auth_john_simple_user['username'],
        'role': 'simple_user'
    }

    assert response_data.get('token') is not None

    response_data['token'] = expected_data['token']

    assert response_data == expected_data
