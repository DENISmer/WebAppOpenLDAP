import pprint
import orjson
import functools

from backend.api.common.groups import Group
from backend.api.tests import datatest as dt

from werkzeug.datastructures import FileStorage


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


def create_user(client, user_data, headers):
    data = orjson.dumps(user_data)
    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=data,
    )

    return response


def delete_user(client, uid, headers):
    response = client.delete(
        f'{dt.Route.USERS.value}/'
        f'{uid}',
        headers=headers,
    )
    return response


def auth(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        client = kwargs['client']
        authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
        headers = {
            'Authorization': f'Bearer {authorized_user["token"]}',
            'Content-Type': 'application/json'
        }
        kwargs['headers'] = headers

        res = func(*args, **kwargs)

        return res

    return wraps


def test_get_user_200(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {'Authorization': f'Bearer {authorized_user["token"]}'}
    response = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_get_bob_webadmins["uid"]}',
        headers=headers
    )

    assert response.status_code == 200

    response_data = orjson.loads(response.data)
    expected_data = dt.data_user_get_bob_webadmins_response

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
    expected_data = dt.data_user_get_john_simple_user_response

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
    del dt.data_user_post_margo_simple_user['jpegPhoto']
    payload = orjson.dumps(dt.data_user_post_margo_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    response_get = client.get(
        f'{dt.Route.USERS.value}/'
        f'{dt.data_user_post_margo_simple_user["uid"]}',
        headers=headers,
    )
    response_get_data = orjson.loads(response.data)

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/posixGroup/'
        f'{dt.data_user_post_margo_simple_user["uid"]}',
        headers=headers,
    )
    response_group_data = orjson.loads(response_group.data)

    client.delete(
        f'{dt.Route.USERS.value}/'
        f'{dt.data_user_post_margo_simple_user["uid"]}',
        headers=headers,
    )

    assert response.status_code == 201

    assert response_get.status_code == 200

    assert response_data == response_get_data

    assert response_group.status_code == 200

    assert response_group_data['memberUid'] == response_data["uid"] \
        and response_group_data['gidNumber'] == response_data["gidNumber"]


@auth
def test_post_user_201_with_photo(client, **kwargs):
    headers = kwargs['headers']
    headers['Content-Type'] += '; multipart/form-data'

    file = FileStorage(
        stream=open('/home/grigoriy/Изображения/flat/1.png', 'rb'),
        filename='flat.png',
        content_type='image/png'
    )

    dt.data_user_post_margo_simple_user.update(
        {'userPassword': 'margo123'}
    )
    # dt.data_user_post_margo_simple_user.update(
    #     {'file_image': file}
    # )
    payload = orjson.dumps(dt.data_user_post_margo_simple_user)
    del dt.data_user_post_margo_simple_user['userPassword']

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        # data=payload,
        files={'my_file': file}
    )
    response_data = orjson.loads(response.data)
    print(response_data)
    expected_data = dt.data_user_post_margo_simple_user

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/posixGroup/'
        f'{dt.data_user_post_margo_simple_user["uid"]}',
        headers=headers,
    )

    client.delete(
        f'{dt.Route.USERS.value}/'
        f'{response_data["uid"]}',
        headers=headers,
    )

    response_group_data = orjson.loads(response_group.data)

    assert response.status_code == 201

    assert response_data == expected_data

    assert response_group.status_code == 200

    assert response_group_data['memberUid'] == response_data["uid"] \
           and response_group_data['gidNumber'] == response_data["gidNumber"]


def test_post_user_data_not_required_field_is_null_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_not_required_fields_is_null_simple_user)

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


def test_post_user_data_only_required_field_201(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_required_fields_simple_user)
    response_free_id = orjson.loads(client.get(
        dt.Route.FREE_IDS.value,
        headers=headers
    ).data)['free_id']

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 201

    response_data = orjson.loads(response.data)
    expected_data = dt.data_user_post_james_data_required_fields_simple_user_response
    expected_data['uidNumber'] = expected_data['gidNumber'] = response_free_id

    response_get = client.get(
        f'{dt.Route.USERS.value}/'
        f'{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers,
    )
    response_get_data = orjson.loads(response_get.data)

    assert response_get.status_code == 200

    assert response_get_data == response_data

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/posixGroup/'
        f'{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers,
    )

    assert response_group.status_code == 200

    client.delete(
        f'{dt.Route.USERS.value}/'
        f'{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers,
    )
    response_group_data = orjson.loads(response_group.data)

    assert response_group_data['memberUid'] == response_data["uid"] \
        and response_group_data['gidNumber'] == response_free_id


def test_post_user_data_incorrect_field_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_incorrect_fields_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'dn': ['The uid parameter is missing'],
                   'mail': ['Missing data for attribute'],
                   'uid': ['The uid does not match the one specified in the dn '
                           'field']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_less_10000_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_less_10000_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'gidNumber': ['gidNumber must be greater than or equal to 10000'],
                   'uidNumber': ['uidNumber must be greater than or equal to 10000']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_without_object_class_ldappublickey_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_not_ldappublickey_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'error': 'ObjectClass Violation',
        'fields': {'objectClass': 'The required objectClass is missing, attribute '
                   "'sshPublicKey' not allowed"},
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_data_without_incorrect_password_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_post_james_data_incorrect_password_simple_user)

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'userPassword': ['The userPassword must be longer than 8 '
                   'characters.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


def test_post_user_missing_data_400(client):
    authorized_user = authorize_user(client, dt.data_user_auth_bob_webadmins)
    headers = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps({})

    response = client.post(
        dt.Route.USERS.value,
        headers=headers,
        data=payload
    )

    assert response.status_code == 400

    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'cn': ['Missing data for required field.'],
                   'dn': ['Missing data for required field.'],
                   'homeDirectory': ['Missing data for required field.'],
                   'objectClass': ['Missing data for required field.'],
                   'sn': ['Missing data for required field.'],
                   'uid': ['Missing data for required field.'],
                   'userPassword': ['Missing data for required field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response_data == expected_data


@auth
def test_patch_user_200(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_user_patch_rambo_simple_user)
    res = create_user(client,  dt.data_user_patch_rambo_for_create, headers)
    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)
    pprint.pprint(response_data)

    if response.status_code != 200:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 200

    response_get = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_simple_user["uid"]}',
        headers=headers
    )
    response_get_data = orjson.loads(response_get.data)
    expected_data = response_get_data

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_data == expected_data


@auth
def test_patch_user_delete_group_create_group_200(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_user_patch_rambo_simple_user)

    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    client.delete(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/'
        f'{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
    )

    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    response_get = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )
    response_get_data = orjson.loads(response_get.data)
    expected_data = response_get_data

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/'
        f'{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
    )
    response_group_data = orjson.loads(response_group.data)

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 200

    assert response_data == expected_data

    assert response_group.status_code == 200

    assert response_group_data['gidNumber'] == response_data['gidNumber'] \
        and response_group_data['memberUid'] == response_data['uid']


@auth
def test_patch_user_not_webadmins_and_current_user_200(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    authorized_user = authorize_user(client, dt.data_user_auth_rambo_simple_user)
    headers_c = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_patch_rambo_not_webadmins_simple_user)
    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers_c,
        data=payload
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 200:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 200

    response_get = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_simple_user["uid"]}',
        headers=headers
    )
    response_get_data = orjson.loads(response_get.data)
    expected_data = response_get_data

    if response_data != expected_data:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_data == expected_data

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )
    response_group_data = orjson.loads(response_group.data)

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_group.status_code == 200

    assert int(response_data["gidNumber"]) == int(response_group_data['gidNumber'])


@auth
def test_patch_user_not_webadmins_and_current_user_none_password_400(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    authorized_user = authorize_user(client, dt.data_user_auth_rambo_simple_user)
    headers_c = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_patch_rambo_not_webadmins_none_user_password_simple_user)
    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers_c,
        data=payload
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 400:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 400

    expected_data = {
        'fields': {'userPassword': ['Field may not be null.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_data == expected_data


@auth
def test_patch_user_change_dn_400(client, **kwargs):
    headers = kwargs['headers']
    create_user(client,  dt.data_user_patch_rambo_for_create, headers)
    payload = orjson.dumps(dt.data_user_patch_rambo_change_dn)
    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 400:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 400

    expected_data = {
        'fields': {'dn': ['Unknown field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_data == expected_data


@auth
def test_patch_user_not_webadmins_and_current_user_more_fields_400(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    authorized_user = authorize_user(client, dt.data_user_auth_rambo_simple_user)
    headers_c = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_patch_rambo_simple_user)
    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers_c,
        data=payload
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 400:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 400

    expected_data = {
        'fields': {'cn': ['Unknown field.'],
            'displayName': ['Unknown field.'],
            'gidNumber': ['Unknown field.'],
            'givenName': ['Unknown field.'],
            'homeDirectory': ['Unknown field.'],
            'loginShell': ['Unknown field.'],
            'objectClass': ['Unknown field.'],
            'postalCode': ['Unknown field.'],
            'sn': ['Unknown field.'],
            'st': ['Unknown field.'],
            'street': ['Unknown field.'],
            'uid': ['Unknown field.'],
            'uidNumber': ['Unknown field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_data == expected_data


@auth
def test_patch_user_not_found_404(client, **kwargs):
    headers = kwargs['headers']

    payload = orjson.dumps(dt.data_user_patch_rambo_simple_user)
    response = client.patch(
        f'{dt.Route.USERS.value}/23423523523',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    assert response.status_code == 404

    expected_data = {'message': 'User not found', 'status': 404}

    assert response_data == expected_data


@auth
def test_patch_user_not_webadmins_and_current_user_more_fields_other_user_403(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    authorized_user = authorize_user(client, dt.data_user_auth_rambo_simple_user)
    headers_c = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    payload = orjson.dumps(dt.data_user_patch_rambo_simple_user)
    response = client.patch(
        f'{dt.Route.USERS.value}/bob',
        headers=headers_c,
        data=payload
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 403:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 403

    expected_data = {'message': 'Insufficient access rights', 'status': 403}

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response_data == expected_data


@auth
def test_patch_user_james_have_only_required_fields_with_none_fields_200(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_user_patch_james_data_required_fields_simple_user)
    res = create_user(client, dt.data_user_post_james_data_required_fields_simple_user, headers)

    response = client.patch(
        f'{dt.Route.USERS.value}/{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    response_get = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers
    )
    response_get_data = orjson.loads(response_get.data)
    expected_data = response_get_data

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/'
        f'{dt.data_user_post_james_data_required_fields_simple_user["uid"]}',
        headers=headers,
    )
    response_group_data = orjson.loads(response_group.data)

    delete_user(client, dt.data_user_post_james_data_required_fields_simple_user["uid"], headers)
    assert response.status_code == 200

    assert response_get.status_code == 200

    assert response_data == expected_data

    assert response_group.status_code == 200

    assert response_group_data['gidNumber'] == response_get_data['gidNumber']

    assert response_group_data['memberUid'] == response_get_data['uid']


@auth
def test_delete_user_204(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    response = client.delete(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )

    if response.status_code != 204:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 204

    response_group = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )
    response_group_data = orjson.loads(response_group.data)
    pprint.pprint(response_group_data)

    assert response_group.status_code == 404

    expected_data = {'message': 'Group not found', 'status': 404}

    assert response_group_data == expected_data


@auth
def test_delete_user_404(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    response = client.delete(
        f'{dt.Route.USERS.value}/dfgdfgdfg',
        headers=headers
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 404:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 404

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    expected_data = {'message': 'User not found', 'status': 404}

    assert response_data == expected_data


@auth
def test_delete_user_simple_user_403(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    authorized_user = authorize_user(client, dt.data_user_auth_rambo_simple_user)
    headers_c = {
        'Authorization': f'Bearer {authorized_user["token"]}',
        'Content-Type': 'application/json'
    }
    response = client.delete(
        f'{dt.Route.USERS.value}/{dt.data_user_get_john_simple_user["uid"]}',
        headers=headers_c
    )
    response_data = orjson.loads(response.data)

    if response.status_code != 403:
        delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 403

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    expected_data = {'message': 'Insufficient access rights', 'status': 403}

    assert response_data == expected_data


@auth
def test_get_list_user_200(client, **kwargs):
    headers = kwargs['headers']

    response = client.get(
        f'{dt.Route.USERS.value}',
        headers=headers
    )
    response_data = orjson.loads(response.data)
    pprint.pprint(response_data)
    assert response.status_code == 200

    assert response_data['page'] == 1 and isinstance(response_data['items'], list)



@auth
def test_create_user_delete_groups(client, **kwargs):
    headers = kwargs['headers']

    # create groups
    response_gr = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=orjson.dumps(dt.data_group_post_margo)
    )

    response_gr2 = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=orjson.dumps(dt.data_group_post_margo)
    )



# THATS ALL