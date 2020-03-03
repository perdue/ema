from cryptography.fernet import Fernet

class Decrypter:
    def __init__(self, key_text):
        self._cipher_suite = Fernet(str.encode(key_text))

    def decrypt(self, ciphered_text):
        bytes = str.encode(ciphered_text)
        unciphered_bytes = self._cipher_suite.decrypt(bytes)
        text = unciphered_bytes.decode('utf-8')
        return text