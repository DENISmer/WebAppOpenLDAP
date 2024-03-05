import unittest

from backend.api.common.crypt_passwd import CryptPasswd


class TestCryptPasswd(unittest.TestCase):
    def setUp(self):
        self.password = 'test'.encode()
        self.crypt_password = b'gAAAAABl5ru1LYES_BjNcT1f5udq5-4Ct_X' \
                              b'QuSwvx2oG9E3AS2Z1Esx1Mog7qZp3Agx_6qIyAPuNiXjbCql97mhq42JNwEC8ww=='  # pass: test
        self.secret_key = ('test' * 8).encode()

    def test_create_password(self):
        crypt_passwd = CryptPasswd(self.password, self.secret_key)
        password = crypt_passwd.crypt()

        self.assertNotEquals(password, None)
        self.assertEqual(type(password), bytes)

    def test_check_password(self):
        crypt_passwd = CryptPasswd(self.crypt_password, self.secret_key)
        decrypt_password = crypt_passwd.decrypt()

        self.assertEqual(decrypt_password, self.password)

    def test_check_password_invalid_crypt_password(self):
        self.invalid_crypt_password = b'gAAAAABl5ru1LYES_BjNcT1f5udq5-4Ct_XQ' \
                                      b'uSwvx2oG9E3AS2Z1Esx1Mog7qZp3Agx_asdasd6qIyAPuNiXjbCql97mhq42JNwEC8ww=='

        crypt_passwd = CryptPasswd(self.invalid_crypt_password, self.secret_key)
        decrypt_password = crypt_passwd.decrypt()

        self.assertEqual(decrypt_password, None)
