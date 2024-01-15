
class Meta:
    pass

class User(object):
    def __init__(self, uid, **kwargs):
        self.dn = kwargs.get('dn')
        self.uidNumber = kwargs.get('uidNumber')
        self.gidNumber = kwargs.get('gidNumber')
        self.uid = uid
        self.sshPublicKey = kwargs.get('sshPublicKey') or []
        self.st = kwargs.get('st')
        self.mail = kwargs.get('mail') or []
        self.street = kwargs.get('street')
        self.cn = kwargs.get('cn')
        self.displayName = kwargs.get('displayName')
        self.givenName = kwargs.get('givenName')
        self.sn = kwargs.get('sn')
        self.userPassword = kwargs.get('userPassword')
        self.objectClass = kwargs.get('objectClass') or []

    def __repr__(self):
        return self.dn

