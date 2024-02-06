import pprint
from abc import ABC


class UserCnAbstract(ABC):
    def __init__(self, *args, **kwargs):
        self.__username = kwargs.get('username')
        self.dn = kwargs.get('dn')
        self.cn = kwargs.get('cn') #or []
        self.objectClass = kwargs.get('objectClass') #or []

        self.gidNumber = kwargs.get('gidNumber')
        if self.gidNumber and type(self.gidNumber) == list:
            self.gidNumber = self.gidNumber[0]

        self.fields = kwargs.get('fields') #or []

    def serialize_data(self, operation) -> dict:

        res = {
            key: getattr(self, key)
            for key, value in self.fields.items()
            if operation in value['operation'] \
               and hasattr(self, key) \
               and getattr(self, key) is not None
        }

        if not operation == 'read' and res.get('dn'):
            del res['dn']

        pprint.pprint(res)

        return res

    def get_username(self):
        return self.__username


class UserLdap(UserCnAbstract):
    def __init__(self, username=None, is_webadmin=False, **kwargs):
        super().__init__(
            **kwargs,
            username=username,
        )

        self.uidNumber = kwargs.get('uidNumber')
        if self.uidNumber and type(self.uidNumber) == list:
            self.uidNumber = self.uidNumber[0]

        self.uid = kwargs.get('uid') #or []
        self.sshPublicKey = kwargs.get('sshPublicKey') #or []
        # if self.sshPublicKey:
        #     self.sshPublicKey = list(map(lambda x: x.encode(), self.sshPublicKey))

        self.st = kwargs.get('st') #or []
        self.mail = kwargs.get('mail') #or []
        self.street = kwargs.get('street') #or []
        self.cn = kwargs.get('cn') #or []

        self.displayName = kwargs.get('displayName')
        if self.displayName and type(self.displayName) == list:
            self.displayName = self.displayName[0]

        self.givenName = kwargs.get('givenName') #or []
        self.sn = kwargs.get('sn') #or []
        self.userPassword = kwargs.get('userPassword') or kwargs.get('password')
        self.objectClass = kwargs.get('objectClass') #or []
        self.postalCode = kwargs.get('postalCode') #or []

        self.homeDirectory = kwargs.get('homeDirectory')
        if self.homeDirectory and type(self.homeDirectory) == list:
            self.homeDirectory = self.homeDirectory[0]

        self.loginShell = kwargs.get('loginShell')
        if self.loginShell and type(self.loginShell):
            self.loginShell = self.loginShell[0]

        self.is_webadmin = is_webadmin
        self.role = kwargs.get('role')

    def __repr__(self):
        return f'DN {self.dn}'


class CnGroupLdap(UserCnAbstract):
    def __init__(self, username=None, *args, **kwargs):
        super().__init__(
            username=username,
            **kwargs,
        )
        self.memberUid = kwargs.get('memberUid')

    def __repr__(self):
        return f'DN {self.dn}'


class GroupWebAdmins:
    def __init__(self, *args, **kwargs):
        self.dn = kwargs.get('dn')
        self.objectClass = kwargs.get('objectClass')
        self.sn = kwargs.get('sn')
        self.member = kwargs.get('member') or []
        self.type = kwargs.get('type')
