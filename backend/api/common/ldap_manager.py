import ldap3


class MetaSingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class LdapServer(metaclass=MetaSingleton):
    def __init__(self, socket: tuple):
        self.server = ldap3.Server(host=socket[0], port=socket[1])


class LdapConnection:

    def __init__(self):
        self.connection = ldap3.Connection()


class LdapManager:
    def __init__(self):
        pass


server = LdapServer(('192.168.1.12', 389))
print('server', server.server)
print('server', id(server.server))

server1 = LdapServer(('192.168.1.12', 389))
print('server1', server1.server)
print('server1', id(server1.server))

server2 = LdapServer(('192.168.1.12', 389))
print('server2', server2.server)
print('server2', id(server2.server))
