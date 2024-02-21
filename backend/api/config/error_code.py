import re

import orjson
import requests

result = re.sub(r'[abc]', lambda match: {'a': '\'', 'b': '\"', 'c': ';', 'd': ':'}.get(match.group(0)), "abcde")
print(result)  # Вывод: 123de, регулярные выражения – ваш верный союзник!


result = re.sub(r'[:\'\";\\/]', lambda match: {'\'': '', '\"': '', ';': '', ':': '', '/': ''}.get(match.group(0)), "attri\"bu:te 'uidNumber' not:; allo/wed ")
print(result)  # Вывод: 123de, регулярные выражения – ваш верный союзник!

url_auth = 'http://127.0.0.1:5000/api/v1/auth/token'
r_auth = requests.post(url_auth,
                       data=orjson.dumps({'username': 'bob', 'userPassword': 'bob'}),
                       headers={'Content-Type': 'application/json'})
data = orjson.loads(r_auth.text)

print(data)
headers = {
    # 'Authorization': f'Bearer {data["token"]}',
    'Content-Type': 'application/json; multipart/form-data',
}
url = 'http://127.0.0.1:5000/api/v1/users'

fin = open('/home/grigoriy/Изображения/flat/1.png', 'rb')
from io import  BytesIO
file_buffer = BytesIO(fin.read())
files = {'file': ('file.png', file_buffer)}

r = requests.post(url, data={"dasdas", "asadasd"}, files=files, headers=headers)

print(r.text)
