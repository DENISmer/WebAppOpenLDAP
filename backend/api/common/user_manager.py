
class Meta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        # print(name, bases)
        # for key, value in namespace.items():
        #     print(key,  value)


class User(metaclass=Meta):
    def __init__(self, username_uid, **kwargs):
        self.dn = kwargs.get('dn')
        self.uidNumber = kwargs.get('uidNumber')
        self.gidNumber = kwargs.get('gidNumber')
        self.uid = kwargs.get('uid') or []
        self.username_uid = username_uid
        self.sshPublicKey = kwargs.get('sshPublicKey') or []
        self.st = kwargs.get('st') or []
        self.mail = kwargs.get('mail') or []
        self.street = kwargs.get('street') or []
        self.cn = kwargs.get('cn') or []
        self.displayName = kwargs.get('displayName') or []
        self.givenName = kwargs.get('givenName') or []
        self.sn = kwargs.get('sn') or []
        self.userPassword = kwargs.get('userPassword') or []
        self.objectClass = kwargs.get('objectClass') or []

    def __repr__(self):
        return self.dn
