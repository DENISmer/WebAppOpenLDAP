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
    authorized_user = authorize_user(client, dt.data_user_auth_john_simple_user)
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


def test_get_user_without_token_401(client):
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_bob_webadmins["uid"]}',
    )

    assert response.status_code == 401

    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Unauthorized Access', 'status': 401}

    assert response_data == expected_data


def test_get_user_not_webadmins_own_profile_200(client):
    authorized_user = authorize_user(client, dt.data_user_auth_john_simple_user)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_john_simple_user["uid"]}',
        headers=headers
    )

    assert response.status_code == 200

    response_data = orjson.loads(response.data)
    expected_data = dt.data_user_get_john_simple_user

    assert response_data == expected_data


def test_post_user_not_webadmins_403(client):
    authorized_user = authorize_user(client, dt.data_user_auth_john_simple_user)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    payload = orjson.dumps(dt.data_user_post_margo_simple_user)
    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 403

    response_data = orjson.loads(response.data)
    expected_data = {
        'message': 'Insufficient access rights',
        'status': 403
    }

    assert response_data == expected_data


def test_post_user_201(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    dt.data_user_post_margo_simple_user.update(
        {'userPassword': 'margo123'}
    )
    payload = orjson.dumps(dt.data_user_post_margo_simple_user)
    del dt.data_user_post_margo_simple_user['userPassword']

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 201

    response_data = orjson.loads(response.data)
    expected_data = dt.data_user_post_margo_simple_user

    assert response_data == expected_data

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/'
        f'{dt.data_user_post_margo_simple_user["uid"]}',
        headers=headers,
    )

    assert response_group.status_code == 200

    client.delete(
        f'{dt.Route.USERS.value}/'
        f'{dt.data_user_post_margo_simple_user["uid"]}',
        headers=headers,
    )

    response_group_data = orjson.loads(response_group.data)

    assert response_group_data['memberUid'] == dt.data_user_post_margo_simple_user["uid"] \
        and response_group_data['gidNumber'] == dt.data_user_post_margo_simple_user["gidNumber"]


def test_post_user_data_non_required_field_is_null_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_non_required_fields_is_null_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'displayName': ['Field may not be null.'],
            'gidNumber': ['Field may not be null.'],
            'givenName': ['Field may not be null.'],
            'loginShell': ['Field may not be null.'],
            'mail': ['Field may not be null.'],
            'postalCode': ['Field may not be null.'],
            'sshPublicKey': ['Field may not be null.'],
            'st': ['Field may not be null.'],
            'street': ['Field may not be null.'],
            'uidNumber': ['Field may not be null.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_all_field_is_null_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_data_all_fields_is_null)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'cn': ['Field may not be null.'],
            'displayName': ['Field may not be null.'],
            'dn': ['Field may not be null.'],
            'gidNumber': ['Field may not be null.'],
            'givenName': ['Field may not be null.'],
            'homeDirectory': ['Field may not be null.'],
            'loginShell': ['Field may not be null.'],
            'mail': ['Field may not be null.'],
            'objectClass': ['Field may not be null.'],
            'postalCode': ['Field may not be null.'],
            'sn': ['Field may not be null.'],
            'sshPublicKey': ['Field may not be null.'],
            'st': ['Field may not be null.'],
            'street': ['Field may not be null.'],
            'uid': ['Field may not be null.'],
            'uidNumber': ['Field may not be null.'],
            'userPassword': ['Field may not be null.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_all_field_is_list_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_data_all_fields_is_list)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'cn': ['Not a valid string.'],
            'displayName': ['Not a valid string.'],
            'dn': ['Not a valid string.'],
            'gidNumber': ['Not a valid integer.'],
            'givenName': ['Not a valid string.'],
            'homeDirectory': ['Not a valid string.'],
            'loginShell': ['Not a valid string.'],
            'postalCode': ['Not a valid integer.'],
            'sn': ['Not a valid string.'],
            'st': ['Not a valid string.'],
            'street': ['Not a valid string.'],
            'uid': ['Not a valid string.'],
            'uidNumber': ['Not a valid integer.'],
            'userPassword': ['Not a valid string.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_all_field_is_list_with_none_empty_row_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_data_all_fields_is_list_with_none_empty_row)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )
    pprint.pprint(orjson.loads(response.data))
    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'cn': ['Not a valid string.'],
            'displayName': ['Not a valid string.'],
            'dn': ['Not a valid string.'],
            'gidNumber': ['Not a valid integer.'],
            'givenName': ['Not a valid string.'],
            'homeDirectory': ['Not a valid string.'],
            'loginShell': ['Not a valid string.'],
            'mail': {'0': ['Not a valid email address.']},
            'postalCode': ['Not a valid integer.'],
            'sn': ['Not a valid string.'],
            'st': ['Not a valid string.'],
            'street': ['Not a valid string.'],
            'uid': ['Not a valid string.'],
            'uidNumber': ['Not a valid integer.'],
            'userPassword': ['Not a valid string.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_non_required_field_201(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_required_fields_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 201

    client.delete(
        f'{dt.Route.USERS.value}/'
        f'{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers,
    )
    pprint.pprint(orjson.loads(response.data))
    response_data = orjson.loads(response.data)
    expected_data = {
    }

    assert response_data == expected_data
