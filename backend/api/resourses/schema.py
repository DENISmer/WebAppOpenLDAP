from marshmallow import Schema, fields


class AuthLDAPSchema(Schema):
    """
    Authentication schema is used to authenticate users
    """

    username = fields.Str(required=True, load_only=True)
    userPassword = fields.Str(required=True, load_only=True)

    def __repr__(self):
        return f"<{AuthLDAPSchema.__name__} {id(self)}>"
