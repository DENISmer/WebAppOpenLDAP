import re

from flask_restful import abort


def validate_str(value) -> bool:
    regex = '^\w+$'
    pattern = re.compile(regex)

    if pattern.search(value) is None:
        return False

    return True


def validate_uid_gid_number(data, errors):
    uid_number = data.get('uidNumber')
    gid_number = data.get('gidNumber')
    if uid_number and gid_number and uid_number != gid_number:
        errors['uidNumber'] = ['uidNumber must be equals to gidNumber']
        errors['gidNumber'] = ['gidNumber must be equals to uidNumber']
    if (uid_number and uid_number < 10000) or (gid_number and gid_number < 10000):
        errors['uidNumber'] = ['uidNumber must be greater than or equal to 10000']
        errors['gidNumber'] = ['gidNumber must be greater than or equal to 10000']


def validate_required_fields(data, errors, declared_field):
    for key, value in data.items():
        required = getattr(declared_field[key], 'required')
        if not getattr(declared_field[key], 'allow_none') \
                and required:
            if not value:
                errors[key] = ['Missing data for required field.']
                continue
            if isinstance(value, list):
                for item in value:
                    if not item:
                        errors[key] = ['Missing data for required field.']
                        break
        else:
            if isinstance(value, list) and value:
                for index, item in enumerate(value):
                    if not item:
                        if not errors.get(key):
                            errors[key] = {}
                        errors[key].update(
                            {f"{index}": ['Missing data for required field.']}
                        )


def validate_uid_dn(data, errors):
    uid, dn = data.get('uid'), data.get('dn')

    dn_dict = {}
    if dn:
        dn_dict = {item[0]: item[1] for item in map(lambda i: i.split('='), dn.split(',')) if len(item) < 3}

    if dn and not dn_dict.get('uid'):
        errors['dn'] = ['The uid parameter is missing']

    if uid and dn and (uid != dn_dict.get('uid')):
        errors['uid'] = ['The uid does not match the one specified in the dn field']


def validate_uid_gid_number_to_unique(ids, uid_number=None, gid_number=None):
    if uid_number in ids or gid_number in ids:
        abort(
            400,
            fields={
                'uidNumber': ['An element with such a uidNumber already exists'],
                'gidNumber': ['An element with such a gidNumber already exists'],
            },
            status=400,
        )
