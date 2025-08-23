from ldap3.core.exceptions import LDAPOperationResult


class LDAPExceptionFlaskError(LDAPOperationResult):
    pass
