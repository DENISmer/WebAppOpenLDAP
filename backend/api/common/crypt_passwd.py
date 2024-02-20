from cryptography.fernet import Fernet
import base64

from backend.api.config import settings


class CryptPasswd:
    def __init__(self, password: bytes, secret_key: bytes):
        if not settings.SECRET_KEY:
            raise Exception('SECRET KEY is None')

        self.__fernet = Fernet(
            base64.b64encode(secret_key)
        )
        self.__password = password

        if not self.__password:
            raise Exception('Password is None')

    def decrypt(self):
        return self.__fernet.decrypt(self.__password)

    def crypt(self):
        return self.__fernet.encrypt(self.__password)
