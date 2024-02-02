import copy
import pprint

from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from marshmallow.schema import SchemaMeta

from backend.api.config import fields as conf_fields


class OuterFields:

    def fetch_fields(self):
        return [field for field in self._declared_fields.keys() if field != 'dn']


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
                # if hasattr(cls._declared_fields[key], 'inner'):
                #     print(id(cls._declared_fields[key].inner))
                    # value_copy_inner = copy.deepcopy(cls._declared_fields[key].inner)
                    # cls._declared_fields[key].inner = value_copy_inner


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
                        # print(key, value['required'])
                        setattr(cls._declared_fields[key], 'allow_none', True)
                        if hasattr(cls._declared_fields[key], 'inner'):
                            setattr(cls._declared_fields[key].inner, 'allow_none', True)
                        # print(key, cls._declared_fields[key])
                    if type_required_fields == 'update':
                        if type_required_fields not in value['operation']:
                            setattr(cls._declared_fields[key], 'dump_only', True)
            # print('------')


class BaseSchema(Schema):
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
        uidNumber = data.get('uidNumber')
        gidNumber = data.get('gidNumber')
        if uidNumber and gidNumber and uidNumber != gidNumber:
            errors['uidNumber'] = ['uidNumber must be equals to gidNumber']
            errors['gidNumber'] = ['gidNumber must be equals to uidNumber']
        if (uidNumber and uidNumber < 10000) or (gidNumber and gidNumber < 10000):
            errors['uidNumber'] = ['uidNumber must be greater than or equal to 10000']
            errors['gidNumber'] = ['gidNumber must be greater than or equal to 10000']

        if errors:
            raise ValidationError(errors)

    @validates('userPassword')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('The userPassword must be longer than 8 characters.')


class SimpleUserSchemaLdapModify(BaseSchema, metaclass=Meta):
    class Meta:
        user_fields = 'simple_user_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{SimpleUserSchemaLdapModify.__name__} {id(self)}>'


class WebAdminsSchemaLdapModify(BaseSchema, metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{WebAdminsSchemaLdapModify.__name__} {id(self)}>'


class WebAdminsSchemaLdapCreate(BaseSchema, metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_fields'
        type_required_fields = 'create'

    def __repr__(self):
        return f'<{WebAdminsSchemaLdapCreate.__name__} {id(self)}>'


class WebAdminsSchemaLdapList(Schema, OuterFields):
    dn = fields.Str(dump_only=True)
    uid = fields.List(fields.Str(dump_only=True), dump_only=True)
    cn = fields.List(fields.Str(dump_only=True), dump_only=True)
    sn = fields.List(fields.Str(dump_only=True), dump_only=True)
    gidNumber = fields.Int(dump_only=True)
    uidNumber = fields.Int(dump_only=True)

    def __repr__(self):
        return f'<{WebAdminsSchemaLdapList.__name__} {id(self)}>'


class AuthUserSchemaLdap(Schema):
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


class GroupBaseSchema(Schema):
    dn = fields.Str()
    gidNumber = fields.Int()
    objectClass = fields.List(fields.Str())
    cn = fields.List(fields.Str())
    memberUid = fields.List(fields.Str())

    @validates('gidNumber')
    def validate_gid_number(self, value):
        if value < 10000:
            raise ValidationError('gidNumber must be greater than or equal to 10000')


class CnGroupSchemaModify(GroupBaseSchema, metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_cn_posixgroup_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{CnGroupSchemaModify.__name__} {id(self)}>'


class CnGroupSchemaCreate(GroupBaseSchema, metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_cn_posixgroup_fields'
        type_required_fields = 'create'

    def __repr__(self):
        return f'<{CnGroupSchemaCreate.__name__} {id(self)}>'


class CnGroupSchemaList(GroupBaseSchema, OuterFields):
    dn = fields.Str(dump_only=True)
    gidNumber = fields.Int(dump_only=True)
    objectClass = fields.List(fields.Str(dump_only=True), dump_only=True)
    cn = fields.List(fields.Str(dump_only=True), dump_only=True)
    memberUid = fields.List(fields.Str(dump_only=True), dump_only=True)

    def __repr__(self):
        return f'<{CnGroupSchemaList.__name__} {id(self)}>'
