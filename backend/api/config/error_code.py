import re

result = re.sub(r'[abc]', lambda match: {'a': '\'', 'b': '\"', 'c': ';', 'd': ':'}.get(match.group(0)), "abcde")
print(result)  # Вывод: 123de, регулярные выражения – ваш верный союзник!


result = re.sub(r'[:\'\";\\/]', lambda match: {'\'': '', '\"': '', ';': '', ':': '', '/': ''}.get(match.group(0)), "attri\"bu:te 'uidNumber' not:; allo/wed ")
print(result)  # Вывод: 123de, регулярные выражения – ваш верный союзник!