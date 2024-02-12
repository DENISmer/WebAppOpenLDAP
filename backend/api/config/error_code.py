# import hashlib
#
#
# h = hashlib.sha1(b'password')
# p = h.hexdigest()
#
# h2 = hashlib.sha1(b'password')
#
# print(h, p, h2, sep=' | ')
# print(h.hexdigest() == h2.hexdigest())
#
# import bcrypt
# salt = bcrypt.gensalt()
# hash = bcrypt.hashpw(b'12345', salt)
# print(hash)
# print(bcrypt.hashpw(b'12345', salt))
# print(bcrypt.checkpw(b'12345', hash))

from cryptography.fernet import Fernet
import base64
import binhex

key1 = '(1v1$%7nf!%=*4_g*3slc0r^%r^rpv3_$)jbnv5f(&('
print(key1[:32])
print('--', len(key1))
key2 = base64.urlsafe_b64encode(bytes(key1[:32].encode()))
key3 = base64.b64encode(bytes(key1[:32].encode()))
print('--1', key2)
print('--1', key3)
key = Fernet.generate_key()
print(type(key))
print(key, len(key),)
# print(base64.b64decode(key))
# print('--', base64.b64decode(key))
# print(len(base64.b64decode(key)))
f = Fernet(key3)
print(token := f.encrypt(b'Hello, world'))
print(f.decrypt(token))

test_key = 'asdasd'
import base64
test_key = base64.b64encode(bytes(test_key.encode()))
print(test_key)