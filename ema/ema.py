# -*- coding: utf-8 -*-

"""EMA module"""

from cryptography.fernet import Fernet

class EMA:
    def __init__(self, host, port, key_text):
        self._host = host
        self._port = port
        self._cipher_suite = Fernet(str.encode(key_text))

    def _decrypt(self, ciphered_text):
        bytes = str.encode(ciphered_text)
        unciphered_bytes = self._cipher_suite.decrypt(bytes)
        text = unciphered_bytes.decode('utf-8')
        print(text)
        return text

    def test_decrypt(self, text):
        self._decrypt(text)

    #def _request()