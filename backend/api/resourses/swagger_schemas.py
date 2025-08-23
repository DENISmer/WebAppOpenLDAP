from flask_restful_swagger_2 import Schema


class StringListAttributesUserModifySchemaSwagger(Schema):
    type = 'string'


class IntListAttributesUserModifySchemaSwagger(Schema):
    type = 'integer'


class AttributesUserModifySchemaSwagger(Schema):
    type = "object"
    properties = {
        "cn": StringListAttributesUserModifySchemaSwagger.array(),
        "displayName": StringListAttributesUserModifySchemaSwagger.array(),
        "gecos": StringListAttributesUserModifySchemaSwagger.array(),
        "givenName": StringListAttributesUserModifySchemaSwagger.array(),
        "homeDirectory": StringListAttributesUserModifySchemaSwagger.array(),
        "loginShell": StringListAttributesUserModifySchemaSwagger.array(),
        "objectClass": StringListAttributesUserModifySchemaSwagger.array(),
        "postalCode": StringListAttributesUserModifySchemaSwagger.array(),
        "sn": StringListAttributesUserModifySchemaSwagger.array(),
        "uid": StringListAttributesUserModifySchemaSwagger.array(),
        "uidNumber": IntListAttributesUserModifySchemaSwagger.array(),
        "gidNumber": IntListAttributesUserModifySchemaSwagger.array(),
    }


class UserModifySchemaSwagger(Schema):
    properties = {
        'attributes': AttributesUserModifySchemaSwagger,
    }


class UserCreateSchemaSwagger(Schema):
    properties = {
        'attributes': AttributesUserModifySchemaSwagger,
        'dn': {
            'type': 'string'
        },
    }


class AttributesGroupModifySchemaSwagger(Schema):
    type = "object"
    properties = {
        "cn": StringListAttributesUserModifySchemaSwagger.array(),
        "gidNumber": IntListAttributesUserModifySchemaSwagger.array(),
        "objectClass": StringListAttributesUserModifySchemaSwagger.array(),
        "memberUid": StringListAttributesUserModifySchemaSwagger.array(),
    }


class GroupCreateSchemaSwagger(Schema):
    properties = {
        'attributes': AttributesGroupModifySchemaSwagger,
        'dn': {
            'type': 'string'
        },
    }


class AuthSchemaSwagger(Schema):
    properties = {
        'username': {
            'type': 'string'
        },
        'userPassword': {
            'type': 'string'
        },
    }
