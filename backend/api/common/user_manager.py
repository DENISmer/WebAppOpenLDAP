
class User(object):
    def __init__(self, dn, uid, **kwargs):
        self.dn = dn
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

    def __repr__(self):
        return self.dn
