# -*- coding: utf-8 -*-

"""Console script for downloading EMA data."""
import _localpath
import argparse
import sys
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import random
from time import sleep
from config import parse_config
from decrypt import Decrypter
from downloader import EMADownloader
import resource_endpoints
from mac import MACGenerator
import builder

def date_fmt():
    return '%Y%m%d'

def parse_args():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')

    required.add_argument(
        "-c", "--conf", required=True, action="store",
        dest="yaml_file",
        help="path to YAML config file"
    )
    optional.add_argument(
        "--debug", default=False, action="store_true",
        dest="debug",
        help="print debug messages"
    )
    optional.add_argument(
        "-o", "--output", required=False, action="store",
        dest="outuri",
        help="output dir as URI [default = file:~/downloads/ema/data, option = drive:<google-drive-dir>]",
        default="file:"+os.path.expanduser("~")+"/downloads/ema/data"
    )
    optional.add_argument(
        "-s", "--startdate", required=False, action="store",
        dest="startdate",
        help="ISO 8601 formatted date to start downloading [YYYYmmdd]",
        default=date.today().strftime(date_fmt())
    )
    optional.add_argument(
        "-e", "--enddate", required=False, action="store",
        dest="enddate",
        help="ISO 8601 formatted date to end downloading [YYYYmmdd]",
        default=None
    )
    parser._action_groups.append(optional)
    return parser.parse_args()

def build_downloader(general_conf, ema_conf, decrypter, debug):
    secret_key = decrypter.decrypt(ema_conf['secret_key'])
    salt_key = decrypter.decrypt(ema_conf['salt_key'])
    salt_value = decrypter.decrypt(ema_conf['salt_value'])
    access_token = decrypter.decrypt(ema_conf['access_token'])
    if (debug):
        print('secret_key:   {}'.format(secret_key))
        print('salt_key:     {}'.format(salt_key))
        print('salt_value:   {}'.format(salt_value))
        print('access_token: {}'.format(access_token))
    mac_generator = MACGenerator(secret_key, salt_key, salt_value, debug)

    downloader = EMADownloader(
        ema_conf['host'],
        ema_conf['port'],
        access_token,
        mac_generator,
        general_conf,
        debug)
    return downloader

def init_downloader(downloader, username, password):
    downloader.authorize(username, password)
    downloader.get_ecu_info()
    downloader.get_view_list()
    downloader.get_view_detail()

def date_str(d, i):
    dt = d + timedelta(days=i)
    return dt.strftime(date_fmt())

def get_power_batch(downloader, drive, date_str):
    dir_name = '{}/{}/{}'.format(drive.outdir(), date_str[:4], date_str[:6])
    file_name = date_str + '-batch.csv.gz'
    full_path = '{}/{}'.format(dir_name, file_name)
    if not drive.gzip_exists(file_name):
        csv = downloader.get_power_batch(date_str)
        drive.write_gzip(csv, full_path)
        secs = random.uniform(0.010, 0.600)
        sleep(secs)

def download(downloader, drive, start_date_str, end_date_str=None):
    if not end_date_str:
        end_date_str = start_date_str
    start_date = datetime.strptime(start_date_str, date_fmt())
    end_date = datetime.strptime(end_date_str, date_fmt())
    num_days = (end_date - start_date).days + 1
    date_list = [date_str(start_date, i) for i in range(num_days)]
    list(map(lambda s: get_power_batch(downloader, drive, s), date_list))

def main():
    """Console script for downloading EMA data."""

    # parse CLI arguments
    args = parse_args()

    # Extract application config and sub-configs
    conf = parse_config(path=args.yaml_file)
    if args.debug:
        print("Using config file: " + str(args.yaml_file))
    general_conf = conf['general']
    ema_conf = conf['ema']

    # Set up downloader
    decrypter = Decrypter(ema_conf['key'])
    drive = builder.build_drive(args.outuri, conf['drive'])
    downloader = build_downloader(general_conf, ema_conf, decrypter, args.debug)
    username = decrypter.decrypt(ema_conf['username'])
    password = decrypter.decrypt(ema_conf['password'])
    init_downloader(downloader, username, password)

    # download data from start date to end date
    download(downloader, drive, args.startdate, args.enddate)

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
