import pprint
import re

import orjson
import requests

result = re.sub(r'[abc]', lambda match: {'a': '\'', 'b': '\"', 'c': ';', 'd': ':'}.get(match.group(0)), "abcde")
print(result)  # Вывод: 123de, регулярные выражения – ваш верный союзник!


result = re.sub(r'[:\'\";\\/]', lambda match: {'\'': '', '\"': '', ';': '', ':': '', '/': ''}.get(match.group(0)), "attri\"bu:te 'uidNumber' not:; allo/wed ")
print(result)  # Вывод: 123de, регулярные выражения – ваш верный союзник!

url_auth = 'http://127.0.0.1:5000/api/v1/auth/token'
r_auth = requests.post(url_auth,
                       data=orjson.dumps({'username': 'tom', 'userPassword': 'tom'}),
                       headers={'Content-Type': 'application/json'})
data = orjson.loads(r_auth.text)

print(data)
headers = {
    'Authorization': f'Bearer {data["token"]}',
    'Content-Type': 'multipart/form-data; boundary=8f3131c59f53f0b362f01b64f052a3db',
}
url = 'http://127.0.0.1:5000/api/v1/users'

fin = open('/home/grig/Изображения/test.png', 'rb')
from io import BytesIO
file_buffer = BytesIO(fin.read())
files = {'file': ('file.png', file_buffer)}
files1 = {'file': fin}
data1 = {"asda": "dasdasd", "dasd": "dasdasd"}
# print(files)
# r = requests.post(url,  files=files, headers=headers)
r = requests.post(url,  files=files, data=data1)
pprint.pprint(r.__dict__)
print(r.text)
