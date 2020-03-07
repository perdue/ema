# -*- coding: utf-8 -*-

"""EMA Data Downloader"""

import os
from cryptography.fernet import Fernet
import requests
import json
from datetime import datetime, timedelta
import pytz
import itertools

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

    def _mkdirs(self, filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _write_file(self, content, filename):
        self._mkdirs(filename)
        print('Writing to '+ filename)
        f = open(filename, "w+")
        f.write(content)
        f.close

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

    def _set_module_info(self, info):
        self._module_info = info

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

    def get_view_detail(self):
        if (self._debug):
            print('get_view_detail()')

        url = self._url(reg_endpoints['viewDetail'])
        if (self._debug):
            print('\turl={}'.format(url))

        data = {
            'access_token': self._access_token,
            'systemId': self._system_id,
            'viewInfoId': self._view_id,
            'language': self._general_conf['content-language']
        }
        self._add_check_code(data)
        if (self._debug):
            print('\tdata={}'.format(data))

        response = self._request(url, data)
        json = response.json()
        detail = json['data']['detail']
        if (self._debug):
            #print('\tdetail={}'.format(detail))
            print(len(detail))
            print('\tdetail={}'.format(detail[:155]))

        record_length = 155
        module_info = {}
        n_modules = int(len(detail)/record_length)
        for i in range(0, n_modules):
            offset = i*record_length
            serial_num = detail[ 0 + offset: 12      + offset]
            chan       = detail[12 + offset: 13      + offset]
            mod_id     = detail[15 + offset: 15 + 32 + offset]
            if (self._debug):
                print('\tserial={}, chan={}, id={}'.format(serial_num, chan, mod_id))
            module_info[mod_id] = {
                'serial_num': serial_num,
                'chan': chan
            }
        self._set_module_info(module_info)
        if (self._debug):
            print('\tmodule_info={}'.format(self._module_info))

        if (self._debug):
            print('get_view_detail()')

    def _iso_str(self, date_str, millis_str):
        tz = pytz.timezone('US/Eastern')
        date = datetime.strptime('{}T04:00:00'.format(date_str), '%Y%m%dT%H:%M:%S').astimezone(tz)
        #print(date.dst())
        timestamp = float(millis_str) / 1000.0
        dt = datetime.fromtimestamp(timestamp) + timedelta(hours=13) - date.dst()
        est_dt = tz.localize(dt)
        return est_dt.isoformat()

    def get_power_batch(self, date_str, outdir):
        if (self._debug):
            print('get_power_batch()')

        url = self._url(prod_endpoints['powerBatch'])
        if (self._debug):
            print('\turl={}'.format(url))

        data = {
            'date': date_str,
            'access_token': self._access_token,
            'systemId': self._system_id,
            'infoId': self._view_id,
            'language': self._general_conf['content-language'],
            'type': str(2)
        }
        self._add_check_code(data)
        if (self._debug):
            print('\tdata={}'.format(data))

        response = self._request(url, data)
        json = response.json()
        data_block = json['data']
        detail = data_block['detail']
        details = str(detail).split('&')
        power = data_block['power'] # probably the total power time series
        times = data_block['time'].split(',')
        date_list = itertools.repeat(date_str, len(times))
        datetimes = list(map(self._iso_str, date_list, times))
        if (self._debug):
            print('\tresponse={}'.format(json))
            #print('\t{}'.format(power))
        rows = []
        for line in details:
            mod_id, values = line.split('/', 1)
            pwr_time_series = values.split(',')
            #print(mod_id)
            #print(pwr_time_series)
            for i in range(0, len(pwr_time_series)):
                mod_info = self._module_info[mod_id]
                row = [
                    mod_id,
                    mod_info['serial_num'],
                    mod_info['chan'],
                    times[i],
                    datetimes[i],
                    pwr_time_series[i]
                ]
                rows.append(','.join(row))

        header = 'mod_id,mod_sn,chan,ts,datetime,power\n'
        csv = header + '\n'.join(sorted(rows))
        filename = '{}/{}-batch.csv'.format(outdir, date_str)
        self._write_file(csv, filename)

        if (self._debug):
            print('get_power_batch()')