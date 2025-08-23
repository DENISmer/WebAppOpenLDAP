import json
import pprint

from flask_restful import request, abort
from flask_restful_swagger_2 import Resource, swagger

from api.common.validators import validate_uid_gid_numbers, validate_dn, validate_attributes
from api.managers.group_ldap_manager_mixin import GroupLDAPManagerMixin
from api.common.decorators import connection_ldap, error_operation_ldap
from api.resourses.swagger_schemas import GroupCreateSchemaSwagger
from api.common.auth_http_token import auth
from api.common.roles import Role


class GroupOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["GroupOpenLDAP"],
        "summary": "Receive group's information",
        "parameters": [
            {
                "name": "cn",
                "description": "Common Name that receive group data",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Return group's information",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "gidNumber": [
                                10011
                            ],
                            "memberUid": [
                                "user"
                            ],
                            "objectClass": [
                                "posixGroup"
                            ]
                        },
                        "dn": "cn=user,ou=Groups,dc=example,dc=com"
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
    def get(self, cn, *args, **kwargs):
        response = GroupLDAPManagerMixin(self.connection).retrieve(cn)
        return response, 200

    def __modify(self, cn, json_data, *args, **kwargs):
        attributes = json_data.get("attributes")
        if not attributes:
            abort(400, message="'Attributes' attribute is not found.")

        group_mixin = GroupLDAPManagerMixin(self.connection)
        group_mixin.modify(cn, attributes)

        response = {
            "attributes": attributes,
            "dn": group_mixin.dn
        }
        return response, 200

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["GroupOpenLDAP"],
        "summary": "Change group's information",
        "parameters": [
            {
                "name": "cn",
                "description": "Common Name that change group data",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": GroupCreateSchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Return changed group's information",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "gidNumber": [
                                10011
                            ],
                            "memberUid": [
                                "user"
                            ],
                            "objectClass": [
                                "posixGroup"
                            ]
                        },
                        "dn": "cn=user,ou=Groups,dc=example,dc=com"
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
    def put(self, cn, *args, **kwargs):
        json_data = request.get_json()
        return self.__modify(cn, json_data, *args, **kwargs)

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["GroupOpenLDAP"],
        "summary": "Change group's information",
        "parameters": [
            {
                "name": "cn",
                "description": "Common Name that change group data",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": GroupCreateSchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Return changed group's information",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "gidNumber": [
                                10011
                            ],
                            "memberUid": [
                                "user"
                            ],
                            "objectClass": [
                                "posixGroup"
                            ]
                        },
                        "dn": "cn=user,ou=Groups,dc=example,dc=com"
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
    def patch(self, cn, *args, **kwargs):
        json_data = request.get_json()
        return self.__modify(cn, json_data, *args, **kwargs)

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["GroupOpenLDAP"],
        "summary": "Delete group's",
        "parameters": [
            {
                "name": "cn",
                "description": "Common Name that change group data",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "204": {
                "description": "Delete group's",
                "examples": {
                    "application/json": {
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
    def delete(self, cn, *args, **kwargs):
        GroupLDAPManagerMixin(self.connection).delete(cn)
        return None, 204


class GroupListOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["GroupOpenLDAP"],
        "summary": "Create group's",
        "parameters": [
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": GroupCreateSchemaSwagger,
            },
        ],
        "responses": {
            "201": {
                "description": "Create group's",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "cn": [
                                "user"
                            ],
                            "gidNumber": [
                                10011
                            ],
                            "memberUid": [
                                "user"
                            ],
                            "objectClass": [
                                "posixGroup"
                            ]
                        },
                        "dn": "cn=user,ou=Groups,dc=example,dc=com"
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

        GroupLDAPManagerMixin(self.connection).create(dn, attributes)

        return json_data, 201

    @auth.login_required(role=[Role.WEB_ADMINS])
    @swagger.doc({
        "tags": ["GroupOpenLDAP"],
        "summary": "Receive group's list information",
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
                "description": "Return group's list",
                "examples": {
                    "application/json": {
                        "attributes": {
                            "items": [
                                {
                                    "attributes": {
                                        "cn": [
                                            "user"
                                        ],
                                        "gidNumber": [
                                            10011
                                        ],
                                        "memberUid": [
                                            "user"
                                        ],
                                        "objectClass": [
                                            "posixGroup"
                                        ]
                                    },
                                    "dn": "cn=user,ou=Groups,dc=example,dc=com"
                                }
                            ],
                            "num_pages": 1,
                            "num_items": 1,
                            "page": 1
                        }
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
        search = request.args.get('search', type=str).strip(" ")
        page = request.args.get('page', type=int, default=1)

        if not search or len(search) < 2:
            return {
                'items': [],
                'num_pages': 0,
                'num_items': 0,
                'page': page,
            }, 200

        response = GroupLDAPManagerMixin(self.connection).search(search, page)
        return response, 200
