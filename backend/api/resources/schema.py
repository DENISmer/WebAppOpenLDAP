import copy
import pprint
import mimetypes
import magic

from marshmallow import Schema, fields, ValidationError, validates, validates_schema, post_dump, post_load, pre_dump, pre_load
from marshmallow.schema import SchemaMeta
from flask_restful import abort
# from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures import FileStorage

from backend.api.common.groups import Group
from backend.api.common.roles import Role
from backend.api.common.route import Route
from backend.api.common.validators import validate_uid_gid_number, validate_required_fields, validate_uid_dn, \
    validate_allowed_file
from backend.api.config import fields as conf_fields


'''
Schema name =  role + route + 'Schema' + 'Ldap' + operation 
'''


class TrimmedString(fields.String):
    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'strip'):
            value = value.strip()
        return super()._deserialize(value, *args, **kwargs)


fields.Str = TrimmedString


class OuterFields:

    def fetch_fields(self):
        return [field for field in self._declared_fields.keys() if field != 'dn']


class MissingFieldsValidation:
    @post_load
    def is_empty_data(self, in_data, **kwargs):
        if not in_data:
            abort(400, message='Fields are missing', status=400)
        return in_data


class PreDumpToList:
    @pre_dump(pass_many=True)
    def to_value_list(self, out_data, many, **kwargs):

        for key, _ in self._declared_fields.items():
            value = getattr(out_data, key)
            if not value:
                value = []
            elif not isinstance(value, list):
                value = [value]

            setattr(out_data, key, value)
        return out_data


class PreDumpFromList:
    @pre_dump
    def from_list(self, out_value, many):
        for key, value in self._declared_fields.items():
            if not isinstance(value, fields.List) \
                    and isinstance(getattr(out_value, key), list) \
                    and len(getattr(out_value, key)) > 0:
                setattr(out_value, key, getattr(out_value, key)[0])
            elif isinstance(value, fields.List) and not getattr(out_value, key):
                setattr(out_value, key, [])
        return out_value


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

                if not cls._declared_fields.get(key):
                    continue

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
                 MissingFieldsValidation,
                 PreDumpFromList):
    dn = fields.Str()
    cn = fields.Str()
    uidNumber = fields.Integer()
    gidNumber = fields.Integer()
    objectClass = fields.List(fields.Str())
    uid = fields.Str()
    sshPublicKey = fields.List(fields.Str())
    st = fields.Str()
    mail = fields.List(fields.Email())
    street = fields.Str()
    displayName = fields.Str()
    givenName = fields.Str()
    sn = fields.Str()
    userPassword = fields.Str(load_only=True, allow_none=False)
    postalCode = fields.Int()
    homeDirectory = fields.Str()
    loginShell = fields.Str()
    jpegPhoto = fields.List(fields.Str())

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}
        validate_uid_gid_number(data, errors)
        validate_required_fields(data, errors, self._declared_fields)
        validate_uid_dn(data, errors)

        if errors:
            raise ValidationError(errors)

    @validates('userPassword')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('The userPassword must be longer than 8 characters.')


class SimpleuserUsersSchemaLdapModify(BaseSchema,
                                      metaclass=Meta):
    class Meta:
        user_fields = 'simple_user_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{SimpleuserUsersSchemaLdapModify.__name__} {id(self)}>'


class WebadminUsersSchemaLdapModify(BaseSchema,
                                    metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{WebadminUsersSchemaLdapModify.__name__} {id(self)}>'


class WebadminUsersSchemaLdapCreate(BaseSchema,
                                    metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_fields'
        type_required_fields = 'create'

    def __repr__(self):
        return f'<{WebadminUsersSchemaLdapCreate.__name__} {id(self)}>'

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}

        uid_number = data.get('uidNumber')
        gid_number = data.get('gidNumber')
        if uid_number and not gid_number:
            errors['gidNumber'] = ['The gidNumber attribute is required']
            # raise ValidationError(errors)
        elif gid_number and not uid_number:
            errors['uidNumber'] = ['The uidNumber attribute is required']
            # raise ValidationError(errors)

        errors.update({
            key: ['Missing data for attribute']
            for key, value in data.items()
            if not value or value == ''
        })
        # validate_required_fields(data, errors, self._declared_fields)
        validate_uid_dn(data, errors)
        validate_uid_gid_number(data, errors)

        if errors:
            raise ValidationError(errors)


class WebadminUsersSchemaLdapList(Schema,
                                  OuterFields,
                                  PreDumpFromList):
    dn = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    cn = fields.Str(dump_only=True)
    sn = fields.Str(dump_only=True)
    gidNumber = fields.Int(dump_only=True)
    uidNumber = fields.Int(dump_only=True)

    def __repr__(self):
        return f'<{WebadminUsersSchemaLdapList.__name__} {id(self)}>'


class AuthSchemaLdapCreate(Schema):
    '''
    Authentication schema is used to authenticate users
    '''
    username = fields.Str(required=True, load_only=True)
    userPassword = fields.Str(required=True, load_only=True)

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}
        validate_required_fields(data, errors, self._declared_fields)
        if errors:
            raise ValidationError(errors)

    def __repr__(self):
        return f'<{AuthSchemaLdapCreate.__name__} {id(self)}>'


class TokenSchemaLdap(Schema):
    token = fields.Str(dump_only=True)
    uid = fields.Str(dump_only=True)
    role = fields.Str(dump_only=True)

    def __repr__(self):
        return f'<{TokenSchemaLdap.__name__} {id(self)}>'


class GroupPosixgroupBaseSchema(Schema,
                                MissingFieldsValidation,
                                PreDumpFromList):
    dn = fields.Str()
    gidNumber = fields.Int()
    objectClass = fields.List(fields.Str())
    cn = fields.Str()
    memberUid = fields.Str()

    @validates('gidNumber')
    def validate_gid_number(self, value):
        if value < 10000:
            raise ValidationError('GidNumber must be greater than or equal to 10000')

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}
        validate_required_fields(data, errors, self._declared_fields)

        if errors:
            raise ValidationError(errors)


class WebadminGroupsPosixgroupSchemaLdapModify(GroupPosixgroupBaseSchema,
                                               metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_cn_posixgroup_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{WebadminGroupsPosixgroupSchemaLdapModify.__name__} {id(self)}>'


class WebadminGroupsPosixgroupSchemaLdapCreate(GroupPosixgroupBaseSchema,
                                               metaclass=Meta):
    class Meta:
        user_fields = 'webadmins_cn_posixgroup_fields'
        type_required_fields = 'create'

    def __repr__(self):
        return f'<{WebadminGroupsPosixgroupSchemaLdapCreate.__name__} {id(self)}>'


class WebadminGroupsPosixgroupSchemaLdapList(Schema,
                                             OuterFields,
                                             PreDumpFromList):
    dn = fields.Str(dump_only=True)
    gidNumber = fields.Int(dump_only=True)
    objectClass = fields.List(fields.Str(dump_only=True), dump_only=True)
    cn = fields.Str(dump_only=True)
    memberUid = fields.Str(dump_only=True)

    def __repr__(self):
        return f'<{WebadminGroupsPosixgroupSchemaLdapList.__name__} {id(self)}>'


class CnGroupOutSchema(WebadminGroupsPosixgroupSchemaLdapList,
                       PreDumpToList):
    def __repr__(self):
        return f'<{CnGroupOutSchema.__name__} {id(self)}>'


class MetaToList(SchemaMeta):
    def __init__(cls, *args, **kwargs):
        super(SchemaMeta, cls).__init__(*args, **kwargs)

        for key, value in cls._declared_fields.items():
            # deep copy
            value_copy = copy.deepcopy(value)
            if not isinstance(value_copy, fields.List):
                new_field = fields.List(value_copy, dump_only=True)
                new_field.inner = value_copy
            else:
                new_field = value_copy
            cls._declared_fields[key] = new_field


class BaseUserOutSchemaToList(BaseSchema,
                              PreDumpToList):
    pass


class UserOutSchemaToList(BaseUserOutSchemaToList,
                          metaclass=MetaToList):
    pass


class BaseCnGroupOutSchemaToList(GroupPosixgroupBaseSchema,
                                 PreDumpToList):
    pass


class CnGroupOutSchemaToList(BaseCnGroupOutSchemaToList,
                             metaclass=MetaToList):
    pass


class FileStorageField(fields.Field):
    # default_error_messages = {
    #     "invalid": "Not a valid image."
    # }

    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        # if value is None:
        #     return None
        #
        # if not isinstance(value, FileStorage):
        #     self.fail("invalid")

        return value


class BaseFilesSchema(Schema):
    jpegPhoto = FileStorageField()
        # fields.Raw(metadata={'type': 'string', 'format': 'binary'})

    @pre_load(pass_many=True)
    def pre_load_data(self, in_data, many, **kwargs):
        new_in_data = {}

        for key in in_data:
            new_in_data[key] = in_data.getlist(key)
            # if not isinstance(self._declared_fields[key], fields.List):
            #     new_in_data[key] = new_in_data[key][:1]

        return new_in_data

    @validates_schema
    def validate_object(self, data, **kwargs):
        errors = {}

        validate_required_fields(data, errors, self._declared_fields)

        for key, files in data.items():

            if not files:
                continue

            for index, file in enumerate(files):

                # mime_type = magic.from_buffer(b''.join(file.stream), mime=True)
                # extension = mimetypes.guess_extension(mime_type)
                # and validate_allowed_file(extension)
                print(file, file.filename)
                if not (file and validate_allowed_file(file.filename)
                ):
                    print(file)
                    if not errors.get(key):
                        errors[key] = {}

                    if not errors[key].get(str(index)):
                        errors[key][str(index)] = []

                    errors[key][str(index)].append('File is not allowed')

        if errors:
            raise ValidationError(errors)

    @post_load(pass_many=True)
    def post_load_data(self, in_data, many, **kwargs):
        for key in in_data:
            if not isinstance(self._declared_fields[key], fields.List):
                in_data[key] = in_data[key][:1]

        return in_data


class WebadminFilesSchemaLdapModify(BaseFilesSchema,
                                    metaclass=Meta):
    class Meta:
        user_fields = 'files_webadmins_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{WebadminFilesSchemaLdapModify.__name__} {id(self)}>'


class SimpleuserFilesSchemaLdapModify(BaseFilesSchema,
                                      metaclass=Meta):
    class Meta:
        user_fields = 'files_webadmins_fields'
        type_required_fields = 'update'

    def __repr__(self):
        return f'<{WebadminFilesSchemaLdapModify.__name__} {id(self)}>'


operation = {
    'post': 'create',
    'get': 'modify',
    'put': 'modify',
    'patch': 'modify',
    'list': 'list'
}
