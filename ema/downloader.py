# -*- coding: utf-8 -*-

"""EMA Data Downloader"""

from cryptography.fernet import Fernet
import requests
import json

from resource_endpoints import *

class EMADownloader:
    def __init__(self, host, port, access_token, key_text, mac_generator, general_conf, debug=False):
        self._host = host
        self._port = str(port)
        self._access_token = access_token
        self._mac_generator = mac_generator
        self._general_conf = general_conf
        self._debug = debug

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

    def _add_check_code(self, data):
        check_code = self._mac_generator.code(data)
        if (self._debug):
            print('_add_check_code()')
            print('\tcheckcode={}'.format(check_code))
            print('_add_check_code()')
        data['checkcode'] = check_code

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
            'password': passwd,
            'language': self._general_conf['content-language'],
            'username': user
        }
        self._add_check_code(data)
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
            'language': self._general_conf['content-language'],
            'userId': self._user_id
        }
        self._add_check_code(data)
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

    def get_view_list(self):
        if (self._debug):
            print('get_view_list()')
        url = self._url(reg_endpoints['viewList'])
        if (self._debug):
            print('\turl={}'.format(url))

        data = {
            'access_token': self._access_token,
            'language': self._general_conf['content-language'],
            'userId': self._user_id
        }
        self._add_check_code(data)
        if (self._debug):
            print('\tdata={}'.format(data))

        response = self._request(url, data)
        json = response.json()
        if (self._debug):
            print('\tresponse={}'.format(json))

        self._set_view_id(json['data']['Right']['viewInfoId'])
        if (self._debug):
            print('\t_view_id={}'.format(self._view_id))
            print('get_view_list()')