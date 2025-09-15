import json
import pprint

from flask_restful import request, abort
from flask_restful_swagger_2 import Resource, swagger

from api.common.validators import validate_uid_gid_numbers, validate_dn, validate_attributes
from api.resourses.swagger_schemas import UserModifySchemaSwagger, UserCreateSchemaSwagger
from api.common.decorators import connection_ldap, error_operation_ldap
from api.managers.user_ldap_manager_mixin import UserLDAPManagerMixin
from api.common.getting_free_id import FreeIdGetter
from api.common.auth_http_token import auth
from api.common.roles import Role


@auth.get_user_roles  # roles
def get_user_roles(user):
    return Role(user['role'])


class UserOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    @swagger.doc({
        "tags": ["UserOpenLDAP"],
        "summary": "Receive user's personal information",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that receive user data",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Return user's personal information",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "displayName": [
                                "User"
                            ],
                            "gecos": [
                                "User User"
                            ],
                            "gidNumber": [
                                10007
                            ],
                            "givenName": [
                                "User"
                            ],
                            "homeDirectory": [
                                "/home/user"
                            ],
                            "loginShell": [
                                "/bin/bash"
                            ],
                            "objectClass": [
                                "inetOrgPerson",
                                "posixAccount",
                                "shadowAccount"
                            ],
                            "postalCode": [
                                124567
                            ],
                            "sn": [
                                "User"
                            ],
                            "uid": [
                                "User"
                            ],
                            "uidNumber": [
                                10007
                            ]
                        },
                        "dn": "uid=user,ou=People,dc=example,dc=com"
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def get(self, uid, *args, **kwargs):
        current_user = auth.current_user()

        # ROLE
        if Role(current_user["role"]) == Role.SIMPLE_USER:
            if current_user["uid"] != uid:
                abort(403, message="Insufficient access rights", status=403)

        response = UserLDAPManagerMixin(self.connection).retrieve(uid)

        return response, 200

    def __modify(self, uid, json_data, *args, **kwargs):
        current_user = auth.current_user()

        attributes = json_data.get("attributes")
        if not attributes:
            abort(400, message="'Attributes' attribute is not found.")

        # ROLE
        if Role(current_user["role"]) == Role.SIMPLE_USER:
            if current_user["uid"] != uid:
                abort(403, message="Insufficient access rights", status=403)

            count_diff_field = len(set(attributes.keys()) \
                                   .difference({"userPassword", "mail", "sshPublicKey"}))

            if count_diff_field > 0:
                abort(403, message="Insufficient access rights", status=403)

        user_mixin = UserLDAPManagerMixin(self.connection)
        user_mixin.modify(uid, attributes)

        user_mixin.delete_attrs(attributes)

        response = {
            "attributes": attributes,
            "dn": user_mixin.dn
        }
        return response, 200

    @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    @swagger.doc({
        "tags": ["UserOpenLDAP"],
        "summary": "Change user's personal information",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that change user data",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": UserModifySchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Return changes user's personal information ",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "displayName": [
                                "User"
                            ],
                            "gecos": [
                                "User User"
                            ],
                            "gidNumber": [
                                10007
                            ],
                            "givenName": [
                                "User"
                            ],
                            "homeDirectory": [
                                "/home/user"
                            ],
                            "loginShell": [
                                "/bin/bash"
                            ],
                            "objectClass": [
                                "inetOrgPerson",
                                "posixAccount",
                                "shadowAccount"
                            ],
                            "postalCode": [
                                124567
                            ],
                            "sn": [
                                "User"
                            ],
                            "uid": [
                                "User"
                            ],
                            "uidNumber": [
                                10007
                            ]
                        },
                        "dn": "uid=user,ou=People,dc=example,dc=com"
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def put(self, uid, *args, **kwargs):
        json_data = request.get_json()
        return self.__modify(uid, json_data, *args, **kwargs)

    @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    @swagger.doc({
        "tags": ["UserOpenLDAP"],
        "summary": "Change user's personal information",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that change user data",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": UserModifySchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Return changes user's personal information ",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "displayName": [
                                "User"
                            ],
                            "gecos": [
                                "User User"
                            ],
                            "gidNumber": [
                                10007
                            ],
                            "givenName": [
                                "User"
                            ],
                            "homeDirectory": [
                                "/home/user"
                            ],
                            "loginShell": [
                                "/bin/bash"
                            ],
                            "objectClass": [
                                "inetOrgPerson",
                                "posixAccount",
                                "shadowAccount"
                            ],
                            "postalCode": [
                                124567
                            ],
                            "sn": [
                                "User"
                            ],
                            "uid": [
                                "User"
                            ],
                            "uidNumber": [
                                10007
                            ]
                        },
                        "dn": "uid=user,ou=People,dc=example,dc=com"
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def patch(self, uid, *args, **kwargs):
        json_data = request.get_json()
        return self.__modify(uid, json_data, *args, **kwargs)

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["UserOpenLDAP"],
        "summary": "Delete user's",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that delete user data",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "204": {
                "description": "Return null",
                "examples": {
                    "application/json": {}
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def delete(self, uid, *args, **kwargs):
        UserLDAPManagerMixin(self.connection).delete(uid)
        return None, 204


class UserListOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["UserOpenLDAP"],
        "summary": "Create user's using personal information",
        "parameters": [
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": UserCreateSchemaSwagger,
            },
        ],
        "responses": {
            "201": {
                "description": "Return created user's personal information",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "displayName": [
                                "User"
                            ],
                            "gecos": [
                                "User User"
                            ],
                            "gidNumber": [
                                10007
                            ],
                            "givenName": [
                                "User"
                            ],
                            "homeDirectory": [
                                "/home/user"
                            ],
                            "loginShell": [
                                "/bin/bash"
                            ],
                            "objectClass": [
                                "inetOrgPerson",
                                "posixAccount",
                                "shadowAccount"
                            ],
                            "postalCode": [
                                124567
                            ],
                            "sn": [
                                "User"
                            ],
                            "uid": [
                                "User"
                            ],
                            "uidNumber": [
                                10007
                            ]
                        },
                        "dn": "uid=user,ou=People,dc=example,dc=com"
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def post(self, *args, **kwargs):
        json_data = request.get_json()

        attributes = validate_attributes(json_data)
        dn = validate_dn(json_data)
        validate_uid_gid_numbers(attributes)

        if not (attributes.get("uidNumber") and attributes.get("gidNumber")):
            free_getter = FreeIdGetter(self.connection)
            numbers = free_getter.get_uid_numbers_from_ldap()
            number = free_getter.get_free_spaces(numbers)
            attributes["uidNumber"] = [number]
            attributes["gidNumber"] = [number]

        user_mixin = UserLDAPManagerMixin(self.connection)
        user_mixin.create(dn, attributes)

        return json_data, 201

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["UserOpenLDAP"],
        "summary": "Receive user's list information",
        "parameters": [
            {
                "name": "search",
                "description": "search data",
                "in": "query",
                "type": "string",
                "required": True
            },
            {
                "default": "1",
                "name": "page",
                "description": "Number of page with data",
                "in": "query",
                "type": "integer",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Return user's list information",
                "examples": {
                    "application/json": {
                        "items": [
                            {
                                "attributes": {
                                    "cn": [
                                        "user"
                                    ],
                                    "gidNumber": [
                                        10011
                                    ],
                                    "sn": [
                                        "user"
                                    ],
                                    "uid": [
                                        "user"
                                    ],
                                    "uidNumber": [
                                        10011
                                    ]
                                },
                                "dn": "uid=user,ou=People,dc=example,dc=com"
                            }
                        ],
                        "num_pages": 1,
                        "num_items": 1,
                        "page": 1
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def get(self):
        search = request.args.get('search', type=str)
        page = request.args.get('page', type=int, default=1)

        if search and len(search) < 2:
            return {
                'items': [],
                'num_pages': 0,
                'num_items': 0,
                'page': page,
            }, 200

        if search:
            search = search.strip(" ")

        response = UserLDAPManagerMixin(self.connection).search(search, page)
        return response, 200
