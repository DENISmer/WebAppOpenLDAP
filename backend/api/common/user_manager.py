from abc import ABC


class UserCnAbstract(ABC):
    def __init__(self, *args, **kwargs):
        self.dn = kwargs.get('dn')
        self.cn = kwargs.get('cn') or []
        self.objectClass = kwargs.get('objectClass') or []

        gid_number = kwargs.get('gidNumber')
        if gid_number:
            self.gidNumber = gid_number[0]

    def serialize_data(self, fields, operation) -> dict:
        res = {
            key: getattr(self, key)
            for key, value in fields.items()
            if operation in value['operation'] \
               and hasattr(self, key) \
               and getattr(self, key)
        }
        return res


class User(UserCnAbstract):
    def __init__(self, username_uid=None, is_webadmin=False, **kwargs):
        super().__init__(
            dn=kwargs.get('dn'),
            cn=kwargs.get('cn'),
            objectClass=kwargs.get('objectClass'),
            gidNumber=kwargs.get('gidNumber'),
        )

        uid_number = kwargs.get('uidNumber')
        if uid_number:
            self.uidNumber = uid_number[0]

        self.uid = kwargs.get('uid') or []
        self.__username_uid = username_uid
        self.sshPublicKey = kwargs.get('sshPublicKey') or []
        self.st = kwargs.get('st') or []
        self.mail = kwargs.get('mail') or []
        self.street = kwargs.get('street') or []
        self.cn = kwargs.get('cn') or []
        self.displayName = kwargs.get('displayName') or []
        self.givenName = kwargs.get('givenName') or []
        self.sn = kwargs.get('sn') or []
        self.userPassword = kwargs.get('userPassword')
        self.objectClass = kwargs.get('objectClass') or []
        self.postalCode = kwargs.get('postalCode') or []

        home_directory = kwargs.get('homeDirectory')
        if home_directory:
            self.homeDirectory = home_directory[0]
        login_shell = kwargs.get('loginShell')
        if login_shell:
            self.loginShell = login_shell[0]

        self.is_webadmin = is_webadmin
        self.role = kwargs.get('role')

    def __repr__(self):
        return self.dn

    def get_username_uid(self):
        return self.__username_uid


class CnUserGroup(UserCnAbstract):
    def __init__(self, *args, **kwargs):
        super().__init__(
            dn=kwargs.get('dn'),
            cn=kwargs.get('cn'),
            objectClass=kwargs.get('objectClass'),
            gidNumber=kwargs.get('gidNumber'),
        )
