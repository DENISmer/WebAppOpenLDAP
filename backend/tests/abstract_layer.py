from ldap3 import Connection, Reader, Writer, ObjectDef
c = Connection('192.168.1.12', 'uid=bob,ou=People,dc=example,dc=com', 'bob', auto_bind=True)
o = ObjectDef('person', c)  # automatic read of the inetOrgPerson structure from schema
r = Reader(c, o, 'uid=bob')  # we don't need to provide a filter because of the objectDef implies '(objectclass=inetOrgPerson)'
r.search()  # populate the reader with the Entries found in the Search

# ake a Writable Cursor from the person_reader Reader Cursor
w = Writer.from_cursor(r)
e = w  # A Cursor is indexed on the Entries collection
print(e)
#ake a Writable Cursor from an LDAP search response, you must specify the objectDef
c.search('o=test', '(objectClass=inetOrgPerson)', attributes=['cn', 'sn', 'givenName'])
w = Writer.from_response(c, c.response, 'person')
e = w[0]
print(e)
#ake a Writable Entry from the first entry of an LDAP search response, an implicit Writer Cursor is created
e = c.entries[0].entry_writable()
print(e)
#ake a new Writable Entry. The Entry remains in "Virtual" state until committed to the DIT
e = w.new('cn=new_entry, o=test')
print(e)