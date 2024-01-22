import pprint
from abc import ABC


class UserCnAbstract(ABC):
    def __init__(self, *args, **kwargs):
        self.dn = kwargs.get('dn')
        self.cn = kwargs.get('cn') or []
        self.objectClass = kwargs.get('objectClass') or []

        self.gidNumber = kwargs.get('gidNumber')
        if self.gidNumber and type(self.gidNumber) == list:
            self.gidNumber = self.gidNumber[0]

        self.fields = kwargs.get('fields')

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
            fields=kwargs.get('fields'),
        )

        self.uidNumber = kwargs.get('uidNumber')
        if self.uidNumber and type(self.uidNumber) == list:
            self.uidNumber = self.uidNumber[0]

        self.uid = kwargs.get('uid') or []
        self.__username_uid = username_uid
        self.sshPublicKey = kwargs.get('sshPublicKey') or []
        self.st = kwargs.get('st') or []
        self.mail = kwargs.get('mail') or []
        self.street = kwargs.get('street') or []
        self.cn = kwargs.get('cn') or []

        self.displayName = kwargs.get('displayName')
        if self.displayName and type(self.displayName) == list:
            self.displayName = self.displayName[0]

        self.givenName = kwargs.get('givenName') or []
        self.sn = kwargs.get('sn') or []
        self.userPassword = kwargs.get('userPassword')
        self.objectClass = kwargs.get('objectClass') or []
        self.postalCode = kwargs.get('postalCode') or []

        self.homeDirectory = kwargs.get('homeDirectory')
        if self.homeDirectory and type(self.homeDirectory) == list:
            self.homeDirectory = self.homeDirectory[0]

        self.loginShell = kwargs.get('loginShell')
        if self.loginShell and type(self.loginShell):
            self.loginShell = self.loginShell[0]

        self.is_webadmin = is_webadmin
        self.role = kwargs.get('role')

    def __repr__(self):
        return self.dn

    def get_username_uid(self):
        return self.__username_uid


class CnGroupLdap(UserCnAbstract):
    def __init__(self, *args, **kwargs):
        super().__init__(
            dn=kwargs.get('dn'),
            cn=kwargs.get('cn'),
            objectClass=kwargs.get('objectClass'),
            gidNumber=kwargs.get('gidNumber'),
        )
