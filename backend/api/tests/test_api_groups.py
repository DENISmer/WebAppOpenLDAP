import pprint

import orjson

from backend.api.common.groups import Group
from backend.api.tests import datatest as dt
from backend.api.tests.test_api_users import auth, create_user, delete_user, authorize_user, delete_group, create_group


@auth
def test_get_group_200(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    response = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'cn': 'rambo',
        'dn': 'cn=rambo,ou=groups,dc=example,dc=com',
        'gidNumber': 10005,
        'memberUid': 'rambo',
        'objectClass': ['posixGroup']
    }

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 200

    assert response_data == expected_data


@auth
def test_get_group_not_webadmins_403(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)

    authorized_data = authorize_user(client, dt.data_user_auth_john_simple_user)
    headers_u = {
        'Authorization': f'Bearer {authorized_data["token"]}'
    }
    response = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers_u
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'message': 'Insufficient access rights',
        'status': 403
    }

    delete_user(client, dt.data_user_patch_rambo_for_create["uid"], headers)
    assert response.status_code == 403

    assert response_data == expected_data


@auth
def test_get_group_type_group_not_found_404(client, **kwargs):
    headers = kwargs['headers']
    response = client.get(
        f'{dt.Route.GROUPS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'error': 'Not Found',
        'message': 'The requested URL was not found on the server. '
                   'If you entered the URL manually please check your spelling and try again',
        'status': 404
    }


    assert response.status_code == 404

    assert response_data == expected_data


@auth
def test_get_group_not_found_404(client, **kwargs):
    headers = kwargs['headers']
    response = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/asdafasf',
        headers=headers
    )
    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Group not found', 'status': 404}

    assert response.status_code == 404

    assert response_data == expected_data


def test_get_group_unauthorized_access_401(client):
    headers = {
        'Authorization': 'Bearer asdfsgaeherfhdhdfh'
    }
    response = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/asdafasf',
        headers=headers
    )
    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Unauthorized Access', 'status': 401}

    assert response.status_code == 401

    assert response_data == expected_data


@auth
def test_post_group_201(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_group_post_rambo)
    response = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)
    expected_data = dt.data_group_post_rambo
    response_group_get = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers
    )
    response_group_get_data = orjson.loads(response_group_get.data)

    delete_group(client, dt.data_group_post_rambo['memberUid'], headers)
    assert response.status_code == 201

    assert response_group_get.status_code == 200

    assert response_data == expected_data == response_group_get_data


@auth
def test_post_group_unique_gid_number_400(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_group_post_rambo)
    client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=orjson.dumps(dt.data_group_post_rambo)
    )
    response = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {
            'gidNumber': ['An element with such a gidNumber already exists']
        },
        'status': 400
    }

    delete_group(client, dt.data_group_post_rambo['memberUid'], headers)
    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_post_group_unique_dn_400(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_group_post_rambo_incorrect_data)
    client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=orjson.dumps(dt.data_group_post_rambo)
    )
    response = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'dn': ['An element with such a dn already exists']},
        'message': 'Invalid attributes',
        'status': 400
    }

    delete_group(client, dt.data_group_post_rambo['memberUid'], headers)
    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_post_group_invalid_object_class_400(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_group_post_rambo_invalid_object_class)
    response = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'objectClass': ['invalid object class asdasdasda']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_post_group_missing_fields_400(client, **kwargs):
    headers = kwargs['headers']
    response = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=orjson.dumps({})
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'cn': ['Missing data for required field.'],
            'dn': ['Missing data for required field.'],
            'gidNumber': ['Missing data for required field.'],
            'objectClass': ['Missing data for required field.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_patch_group_200(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    payload = orjson.dumps(dt.data_group_patch_rambo)
    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    response_user_get = client.get(
        f'{dt.Route.USERS.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers
    )
    response_user_get_data = orjson.loads(response_user_get.data)

    response_group_get = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers
    )
    response_group_get_data = orjson.loads(response_group_get.data)

    delete_user(client, dt.data_user_patch_rambo_for_create['uid'], headers)
    assert response.status_code == 200

    assert response_group_get.status_code == 200

    assert response_data == response_group_get_data

    assert response_user_get.status_code == 200

    assert response_user_get_data['gidNumber'] \
           == response_data['gidNumber'] == response_group_get_data['gidNumber']


@auth
def test_patch_group_not_found_404(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    payload = orjson.dumps(dt.data_group_patch_rambo)
    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/asdfsfsdfsdf',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Group not found', 'status': 404}

    delete_user(client, dt.data_user_patch_rambo_for_create['uid'], headers)
    assert response.status_code == 404

    assert response_data == expected_data


@auth
def test_patch_group_not_webadmins_403(client, **kwargs):
    headers = kwargs['headers']
    authorized_data = authorize_user(client, dt.data_user_auth_john_simple_user)
    headers_u = {
        'Authorization': f'Bearer {authorized_data["token"]}',
        'Content-Type': 'application/json'
    }
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    payload = orjson.dumps(dt.data_group_patch_rambo)
    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers_u,
        data=payload
    )
    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Insufficient access rights', 'status': 403}

    delete_user(client, dt.data_user_patch_rambo_for_create['uid'], headers)
    assert response.status_code == 403

    assert response_data == expected_data


@auth
def test_patch_group_missing_fields_400(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
        data=orjson.dumps({})
    )
    response_data = orjson.loads(response.data)
    expected_data = {'message': 'Fields are missing', 'status': 400}

    delete_user(client, dt.data_user_patch_rambo_for_create['uid'], headers)
    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_patch_group_two_member_uid_400(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
        data=orjson.dumps(dt.data_group_patch_several_member_uid)
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'memberUid': ['Not a valid string.']},
        'message': 'Invalid attributes',
        'status': 400
    }

    delete_user(client, dt.data_user_patch_rambo_for_create['uid'], headers)
    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_patch_group_invalid_object_class_400(client, **kwargs):
    headers = kwargs['headers']
    create_user(client, dt.data_user_patch_rambo_for_create, headers)
    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_user_patch_rambo_for_create["uid"]}',
        headers=headers,
        data=orjson.dumps(dt.data_group_patch_rambo_invalid_object_class)
    )
    response_data = orjson.loads(response.data)
    expected_data = {
        'fields': {'objectClass': ['invalid class in objectClass attribute: asdafaf']},
        'message': 'Invalid attributes',
        'status': 400
    }

    delete_user(client, dt.data_user_patch_rambo_for_create['uid'], headers)
    assert response.status_code == 400

    assert response_data == expected_data


@auth
def test_patch_group_with_none_fields_200(client, **kwargs):
    headers = kwargs['headers']
    create_group(client, dt.data_group_post_rambo_for_create_without_member_uid, headers)
    payload = orjson.dumps(dt.data_group_patch_rambo)

    response = client.patch(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/rambo',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    response_group_get = client.get(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/rambo',
        headers=headers
    )
    response_group_get_data = orjson.loads(response_group_get.data)

    delete_group(client, 'rambo', headers)
    assert response.status_code == 200

    assert response_group_get.status_code == 200

    assert response_data == response_group_get_data


@auth
def test_delete_group_204(client, **kwargs):
    headers = kwargs['headers']
    payload = orjson.dumps(dt.data_group_post_rambo)
    response = client.post(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}',
        headers=headers,
        data=payload
    )
    response_data = orjson.loads(response.data)

    assert response.status_code == 201

    response_delete = client.delete(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers
    )

    assert response_delete.status_code == 204


@auth
def test_delete_group_not_found_404(client, **kwargs):
    headers = kwargs['headers']
    response_delete = client.delete(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers
    )
    response_delete_data = orjson.loads(response_delete.data)
    expected_data = {'message': 'Group not found', 'status': 404}

    assert response_delete.status_code == 404

    assert response_delete_data == expected_data


def test_delete_group_not_webadmins_403(client):
    authorized_data = authorize_user(client, dt.data_user_auth_john_simple_user)
    headers_u = {
        'Authorization': f'Bearer {authorized_data["token"]}',
        'Content-Type': 'application/json'
    }
    response_delete = client.delete(
        f'{dt.Route.GROUPS.value}/{Group.POSIXGROUP.value}/{dt.data_group_post_rambo["memberUid"]}',
        headers=headers_u
    )
    response_delete_data = orjson.loads(response_delete.data)
    expected_data = {'message': 'Insufficient access rights', 'status': 403}

    assert response_delete.status_code == 403

    assert response_delete_data == expected_data


# THATS ALL