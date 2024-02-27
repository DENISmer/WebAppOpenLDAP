from flask_restful import Resource

from backend.api.common.auth_http_token import auth
from backend.api.common.decorators import connection_ldap
from backend.api.common.getting_free_id import GetFreeId
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role


class FreeIdsOpenLDAPResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    @auth.login_required(role=[Role.WEB_ADMIN])
    @connection_ldap
    def get(self, *args, **kwargs):
        conn_ldap = UserManagerLDAP(connection=self.connection)
        ids = conn_ldap.get_id_numbers()
        free_id = conn_ldap.get_free_id_number()
        get_free_id = GetFreeId()
        get_free_id.delete_from_reserved(free_id)

        return {'ids': list(ids), 'free_id': free_id}, 200