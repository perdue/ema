# -*- coding: utf-8 -*-

"""EMA module"""

from cryptography.fernet import Fernet
import requests
import json
#import resource_endpoints
from resource_endpoints import *

class EMA:
    def __init__(self, host, port, key_text, general_conf):
        self._host = host
        self._port = str(port)
        self._cipher_suite = Fernet(str.encode(key_text))
        self._general_conf = general_conf

    def _decrypt(self, ciphered_text):
        bytes = str.encode(ciphered_text)
        unciphered_bytes = self._cipher_suite.decrypt(bytes)
        text = unciphered_bytes.decode('utf-8')
        return text

    def test_decrypt(self, text):
        self._decrypt(text)


    def _headers(self):
        headers = {
            'Content-Type': self._general_conf['content-type'],
            'User-Agent': self._general_conf['user-agent'],
            'Content-Language': self._general_conf['content-language']
        }
        return headers

    def _url(self, endpoint):
        return build_url(self._host, self._port, endpoint)

    def _request(self, url, data):
        return requests.post(url, data=data, headers=self._headers())

    def getVersion(self):
        url = 'http://' + \
              self._host + ':' + self._port + \
              '/' + BASE + '/EMAApp/version.xml'

        print(url)              
        response = requests.get(url)
        print(response.text)
        return response

    def _set_access_token(self, token):
        self._access_token = token

    def _set_system_id(self, id):
        self._system_id = id

    def _set_user_id(self, id):
        self._user_id = id

    def _set_ecu_id(self, id):
        self._ecu_id

    def _set_view_id(self, id):
        self._view_id

    def authorize(self, token, user, passwd, checkcode):
        url = self._url(reg_endpoints['checkUser'])
        print(url)
        data = {
            'access_token': self._decrypt(token),
            'password': self._decrypt(passwd),
            'language': self._general_conf['content-language'],
            'checkcode': self._decrypt(checkcode),
            'username': self._decrypt(user)
            #'appid': self._decrypt(appid)
        }
        print(data)
        response = self._request(url, data)
        json = response.json()
        print(json)
        #self._set_access_token(json['access_token'])

    def _extract_view_id(self, data):
        parsed = json.loads(data)
        print(data)

    def login(self, username, password):
        url = self._url(user_endpoints['login'])
        data = {
            'username': self._decrypt(username),
            'password': self._decrypt(password),
            'access_token': self._access_token
        }
        response = self._request(url, data)
        print(response.text)
#        json_string = response.json()['data']
#        parsed = json.loads(json_string)
#        print(json_string)
#        print(parsed)
#        print(json.loads(parsed['systemId'])[0])
#        _extract_view_id(parsed['viewList'])

