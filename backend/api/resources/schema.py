import copy
import pprint

from marshmallow import Schema, fields, ValidationError, validates, validates_schema, post_dump, post_load
from marshmallow.schema import SchemaMeta
from flask_restful import abort

from backend.api.common.validators import validate_uid_gid_number, validate_required_fields
from backend.api.config import fields as conf_fields


class OuterFields:

    def fetch_fields(self):
        return [field for field in self._declared_fields.keys() if field != 'dn']


class MissingFieldsValidation:
    @post_load
    def is_empty_data(self, in_data, **kwargs):
        if not in_data:
            abort(400, fields_error='Fields are missing', status=400)
        return in_data


class Meta(SchemaMeta):
    def __init__(cls, *args, **kwargs):
        super(SchemaMeta, cls).__init__(*args, **kwargs)

        if hasattr(cls, 'Meta'):
            meta_class = getattr(cls, 'Meta')
            if not hasattr(meta_class, 'user_fields'):
                raise AttributeError('Meta class has not attribute \'user_fields\'')

            if not hasattr(meta_class, 'type_required_fields'):
                raise AttributeError('Meta class has not attribute \'type_required_fields\'')

            type_required_fields = getattr(meta_class, 'type_required_fields')

            if type_required_fields not in ('update', 'create', 'list'):
                raise AttributeError('type_required_fields must has the \'update\' anb \'create\'')

            user_fields = getattr(meta_class, 'user_fields')

            if not hasattr(conf_fields, user_fields):
                raise AttributeError(f'conf_fields has not attribute \'{user_fields}\'')

            _fields = getattr(conf_fields, user_fields)

            for key, value in _fields['fields'].items():
                # deep copy
                value_copy = copy.deepcopy(cls._declared_fields[key])
                cls._declared_fields[key] = value_copy
                # end deep copy

                if type_required_fields == 'list':
                    setattr(cls._declared_fields[key], 'dump_only', True)
                else:
                    if 'read' in value['required']:
                        setattr(cls._declared_fields[key], 'dump_only', True)

                    if type_required_fields in value['required']:
                        setattr(cls._declared_fields[key], 'required', True)

                        if hasattr(cls._declared_fields[key], 'inner'):
                            setattr(cls._declared_fields[key].inner, 'required', True)

                    if 'create' not in value['required'] and type_required_fields == 'update':

                        setattr(cls._declared_fields[key], 'allow_none', True)
                        if hasattr(cls._declared_fields[key], 'inner'):
                            setattr(cls._declared_fields[key].inner, 'allow_none', True)

                    if type_required_fields == 'update':
                        if type_required_fields not in value['operation']:
                            setattr(cls._declared_fields[key], 'dump_only', True)


class BaseSchema(Schema,
                 MissingFieldsValidation):
    dn = fields.Str()
    cn = fields.List(fields.Str())
    uidNumber = fields.Integer()
    gidNumber = fields.Integer()
    objectClass = fields.List(fields.Str())
    uid = fields.List(fields.Str())
    sshPublicKey = fields.List(fields.Str())
    st = fields.List(fields.Str())
    mail = fields.List(fields.Email())
    street = fields.List(fields.Str())
    displayName = fields.Str()
    givenName = fields.List(fields.Str())
    sn = fields.List(fields.Str())
    userPassword = fields.Str(load_only=True)
    postalCode = fields.List(fields.Int())
    homeDirectory = fields.Str()
    loginShell = fields.Str()

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}

        validate_uid_gid_number(data, errors)
        validate_required_fields(data, errors, self._declared_fields)

        if errors:
            raise ValidationError(errors)

    @validates('userPassword')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('The userPassword must be longer than 8 characters.')


class BaseOutSchema:

    @post_dump(pass_many=True)
    def to_list(self, out_data, **kwargs):
        pprint.pprint(out_data)
        for key, value in out_data.items():

            if not value:
                value = []
            elif not isinstance(value, list):
                value = [value]

            out_data[key] = value

        return out_data


class SimpleUserSchemaLdapModify(BaseSchema,
                                 BaseOutSchema,
                                 metaclass=Meta):
    class Meta:
        user_fields = 'simple_user_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{SimpleUserSchemaLdapModify.__name__} {id(self)}>'


class WebAdminsSchemaLdapModify(BaseSchema,
                                BaseOutSchema,
                                metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{WebAdminsSchemaLdapModify.__name__} {id(self)}>'


class WebAdminsSchemaLdapCreate(BaseSchema,
                                BaseOutSchema,
                                metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_fields'
        type_required_fields = 'create'

    def __repr__(self):
        return f'<{WebAdminsSchemaLdapCreate.__name__} {id(self)}>'

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}
        
        uid_number = data.get('uidNumber')
        gid_number = data.get('gidNumber')
        if uid_number and not gid_number:
            errors['gidNumber'] = ['The gidNumber attribute is required']
            raise ValidationError(errors)
        elif gid_number and not uid_number:
            errors['uidNumber'] = ['The uidNumber attribute is required']
            raise ValidationError(errors)

        errors.update({
            key: ['Missing data for attribute']
            for key, value in data.items()
            if not value or value == ''
        })
        
        validate_uid_gid_number(data, errors)

        if errors:
            raise ValidationError(errors)


class WebAdminsSchemaLdapList(Schema,
                              OuterFields):
    dn = fields.Str(dump_only=True)
    uid = fields.List(fields.Str(dump_only=True), dump_only=True)
    cn = fields.List(fields.Str(dump_only=True), dump_only=True)
    sn = fields.List(fields.Str(dump_only=True), dump_only=True)
    gidNumber = fields.Int(dump_only=True)
    uidNumber = fields.Int(dump_only=True)

    def __repr__(self):
        return f'<{WebAdminsSchemaLdapList.__name__} {id(self)}>'


class AuthUserSchemaLdap(Schema):
    '''
    Authentication schema is used to authenticate users
    '''
    username = fields.Str(required=True, load_only=True)
    userPassword = fields.Str(required=True, load_only=True)

    def __repr__(self):
        return f'<{AuthUserSchemaLdap.__name__} {id(self)}>'


class TokenSchemaLdap(Schema):
    token = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    role = fields.Str(dump_only=True)

    def __repr__(self):
        return f'<{TokenSchemaLdap.__name__} {id(self)}>'


class GroupBaseSchema(Schema,
                      MissingFieldsValidation):
    dn = fields.Str()
    gidNumber = fields.Int()
    objectClass = fields.List(fields.Str())
    cn = fields.List(fields.Str())
    memberUid = fields.List(fields.Str())

    @validates('gidNumber')
    def validate_gid_number(self, value):
        if value < 10000:
            raise ValidationError('gidNumber must be greater than or equal to 10000')

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}
        validate_required_fields(data, errors, self._declared_fields)

        if errors:
            raise ValidationError(errors)


class CnGroupSchemaModify(GroupBaseSchema,
                          BaseOutSchema,
                          metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_cn_posixgroup_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{CnGroupSchemaModify.__name__} {id(self)}>'


class CnGroupSchemaCreate(GroupBaseSchema,
                          BaseOutSchema,
                          metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_cn_posixgroup_fields'
        type_required_fields = 'create'

    def __repr__(self):
        return f'<{CnGroupSchemaCreate.__name__} {id(self)}>'


class CnGroupSchemaList(GroupBaseSchema,
                        OuterFields):
    dn = fields.Str(dump_only=True)
    gidNumber = fields.Int(dump_only=True)
    objectClass = fields.List(fields.Str(dump_only=True), dump_only=True)
    cn = fields.List(fields.Str(dump_only=True), dump_only=True)
    memberUid = fields.List(fields.Str(dump_only=True), dump_only=True)

    def __repr__(self):
        return f'<{CnGroupSchemaList.__name__} {id(self)}>'


class CnGroupOutSchema(CnGroupSchemaList,
                       BaseOutSchema):
    def __repr__(self):
        return f'<{CnGroupOutSchema.__name__} {id(self)}>'
