# -*- coding: utf-8 -*-

"""EMA Downloader"""

from cryptography.fernet import Fernet
import requests
import json

from resource_endpoints import *

class EMADownloader:
    def __init__(self, host, port, access_token, key_text, general_conf, debug=False):
        self._host = host
        self._port = str(port)
        self._cipher_suite = Fernet(str.encode(key_text))
        self._access_token = self._decrypt(access_token)
        self._general_conf = general_conf
        self._debug = debug

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
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
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

    def _set_user_id(self, id):
        self._user_id = id

    def _set_system_id(self, id):
        self._system_id = id

    def _set_ecu_id(self, id):
        self._ecu_id = id

    def _set_view_id(self, id):
        self._view_id = id

    def authorize(self, user, passwd):
        if (self._debug):
            print('authorize()')
        url = self._url(reg_endpoints['checkUser'])
        if (self._debug):
            print('\turl={}'.format(url))
        data = {
            'access_token': self._access_token,
            'password': self._decrypt(passwd),
            'language': self._general_conf['content-language'],
            'checkcode': check_codes['checkUser'],
            'username': self._decrypt(user)
        }
        if (self._debug):
            print('\tdata={}'.format(data))
        response = self._request(url, data)
        json = response.json()
        if (self._debug):
            print('\tresponse={}'.format(json))
        self._set_user_id(json['data']['user']['id'])
        if (self._debug):
            print('\t_user_id={}'.format(self._user_id))
        if (self._debug):
            print('authorize()')
        
    def get_ecu_info(self):
        if (self._debug):
            print('get_ecu_info()')
        url = self._url(reg_endpoints['ecuInfo'])
        if (self._debug):
            print('\turl={}'.format(url))
        data = {
            'access_token': self._access_token,
            'checkcode': check_codes['ecuInfo'],
            'language': self._general_conf['content-language'],
            'userId': self._user_id
        }
        if (self._debug):
            print('\tdata={}'.format(data))
        response = self._request(url, data)
        json = response.json()
        if (self._debug):
            print('\tresponse={}'.format(json))

        for k in json['data'].keys():
            if (self._user_id in k):
                self._set_system_id(json['data'][k]['systemId'])
                self._set_ecu_id(json['data'][k]['ecuId'])

        if (self._debug):
            print('\t_system_id={}'.format(self._system_id))
            print('\t_ecu_id={}'.format(self._ecu_id))
        if (self._debug):
            print('get_ecu_info()')

#    def _extract_view_id(self, data):
#        parsed = json.loads(data)
#        print(data)

#    def login(self, username, password):
#        url = self._url(user_endpoints['login'])
#        data = {
#            'username': self._decrypt(username),
#            'password': self._decrypt(password),
#            'access_token': self._access_token
#        }
#        response = self._request(url, data)
#        print(response.text)
#        json_string = response.json()['data']
#        parsed = json.loads(json_string)
#        print(json_string)
#        print(parsed)
#        print(json.loads(parsed['systemId'])[0])
#        _extract_view_id(parsed['viewList'])

