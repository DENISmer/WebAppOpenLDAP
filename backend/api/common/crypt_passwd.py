from __future__ import annotations

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

import base64


class CryptPasswd:
    def __init__(self, password: bytes, secret_key: bytes):
        if not secret_key:
            raise Exception('SECRET KEY is None')
        if not password:
            raise Exception('Password is None')

        self.__fernet = Fernet(
            base64.b64encode(secret_key)
        )
        self.__password = password

    def decrypt(self) -> bytes | None:
        try:
            return self.__fernet.decrypt(self.__password)
        except InvalidToken:
            return None

    def crypt(self) -> bytes:
        return self.__fernet.encrypt(self.__password)
