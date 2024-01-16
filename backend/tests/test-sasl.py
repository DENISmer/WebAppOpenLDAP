from ldap3 import Server, Connection, ALL
s = Server('0.0.0.0', get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema
c = Connection(s)
c.open()  # establish connection without performing any bind (equivalent to ANONYMOUS bind)
print(s.info.supported_sasl_mechanisms)