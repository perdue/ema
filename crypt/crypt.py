# -*- coding: utf-8 -*-

"""Encrypt utility module."""

import os
from cryptography.fernet import Fernet

def generate(appid, username, password, key):
    if key is None:
        key = Fernet.generate_key()
    print(key)

    cipher_suite = Fernet(key)
    ciphered_appid = cipher(appid, cipher_suite)
    ciphered_username = cipher(username, cipher_suite)
    ciphered_password = cipher(password, cipher_suite)

    check(ciphered_appid, cipher_suite)
    check(ciphered_username, cipher_suite)
    check(ciphered_password, cipher_suite)

    return key, ciphered_appid, ciphered_username, ciphered_password

def cipher(text, cipher_suite):
    ciphered_text = cipher_suite.encrypt(str.encode(text)) # required to be bytes
    print(ciphered_text)
    return ciphered_text

def check(bytes, cipher_suite):
    unciphered_text = (cipher_suite.decrypt(bytes))
    print(unciphered_text)

def write_key(key, filename):
    mkdirs(filename)
    print('Writing key to ' + filename)
    f = open(filename, "w+")
    f.write(statement('EMA_KEY', key))
    f.close
    os.chmod(filename, 0o600)

def write_credentials(appid, username, password, filename):
    mkdirs(filename)
    print('Writing credentials to ' + filename)
    f = open(filename, "w+")
    f.write(statement('EMA_APPID', appid))
    f.write(statement('EMA_USERNAME', username))
    f.write(statement('EMA_PASSWORD', password))
    f.close
    os.chmod(filename, 0o600)

def mkdirs(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    os.chmod(dirname, 0o700)

def statement(env_var, credential):
    return ('export ' + env_var + '="' + credential.decode('utf-8') + '"' + '\n')
