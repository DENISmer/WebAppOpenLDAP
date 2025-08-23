from flask_restful import abort

from api.conf import settings

def validate_dn(json_data):
    dn = json_data.get("dn")
    if not dn:
        abort(400, message="'dn' attribute is not found.")

    return dn


def validate_attributes(json_data):
    attributes = json_data.get("attributes")
    if not attributes:
        abort(400, message="'Attributes' attribute is not found.")

    return attributes


def validate_uid_gid_numbers(attributes):
    uid_number, gid_number = attributes.get("uidNumber"), attributes.get("gidNumber")

    if uid_number and not gid_number:
        attributes["gidNumber"] = uid_number
    elif not uid_number and gid_number:
        attributes["uidNumber"] = gid_number

    if uid_number and gid_number and uid_number != gid_number:
        abort(400, message="uidNumber and gidNumber must be equals", )

    if (uid_number and uid_number[0] < 10000) or (gid_number and gid_number[0] < 10000):
        abort(400, message="uidNumber or gidNumber must be greater than or equal to 10000")


def validate_allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS
