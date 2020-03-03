# -*- coding: utf-8 -*-

"""Encrypt utility module."""

import os
from cryptography.fernet import Fernet

def generate(access_token,
             secret_key,
             salt_key,
             salt_value,
             username,
             password,
             key):
    if key is None:
        key = Fernet.generate_key()
    print(key)

    cipher_suite = Fernet(key)
    ciphered_access_token = cipher(access_token, cipher_suite)
    ciphered_secret_key = cipher(secret_key, cipher_suite)
    ciphered_salt_key = cipher(salt_key, cipher_suite)
    ciphered_salt_value = cipher(salt_value, cipher_suite)
    ciphered_username = cipher(username, cipher_suite)
    ciphered_password = cipher(password, cipher_suite)

    check(ciphered_access_token, cipher_suite)
    check(ciphered_secret_key, cipher_suite)
    check(ciphered_salt_key, cipher_suite)
    check(ciphered_salt_value, cipher_suite)
    check(ciphered_username, cipher_suite)
    check(ciphered_password, cipher_suite)

    return ciphered_access_token, ciphered_secret_key, ciphered_salt_key, ciphered_salt_value, ciphered_username, ciphered_password, key

def cipher(text, cipher_suite):
    ciphered_text = cipher_suite.encrypt(str.encode(text)) # required to be bytes
    #print(ciphered_text)
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

def write_credentials(access_token,
                      secret_key,
                      salt_key,
                      salt_value,
                      username,
                      password,
                      filename):
    mkdirs(filename)
    print('Writing credentials to ' + filename)
    f = open(filename, "w+")
    f.write(statement('EMA_ACCESS_TOKEN', access_token))
    f.write(statement('EMA_SECRET_KEY', secret_key))
    f.write(statement('EMA_SALT_KEY', salt_key))
    f.write(statement('EMA_SALT_VALUE', salt_value))
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
