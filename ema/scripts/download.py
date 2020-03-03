# -*- coding: utf-8 -*-

"""Console script for ema."""
import _localpath
import argparse
import sys
from config import parse_config
from decrypt import Decrypter
from downloader import EMADownloader
import resource_endpoints
from mac import MACGenerator

def main():
    """Console script for ema."""

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
    parser._action_groups.append(optional)
    args = parser.parse_args()

    conf = parse_config(path=args.yaml_file)

    print("Using config file: " +
          str(args.yaml_file))

    ema_conf = conf['ema']
    decrypter = Decrypter(ema_conf['key'])

    secret_key = decrypter.decrypt(ema_conf['secret_key'])
    salt_key = decrypter.decrypt(ema_conf['salt_key'])
    salt_value = decrypter.decrypt(ema_conf['salt_value'])
    mac_generator = MACGenerator(secret_key, salt_key, salt_value, args.debug)

    downloader = EMADownloader(
        ema_conf['host'],
        ema_conf['port'],
        decrypter.decrypt(ema_conf['access_token']),
        ema_conf['key'],
        mac_generator,
        conf['general'],
        args.debug)
    
    if (args.debug):
        resource_endpoints.check_endpoints(ema_conf['host'], ema_conf['port'])


#    downloader.getVersion()
    username = decrypter.decrypt(ema_conf['username'])
    password = decrypter.decrypt(ema_conf['password'])
    downloader.authorize(username, password)

    downloader.get_ecu_info()
    downloader.get_view_list()
    downloader.get_power_batch('20191201')
    downloader.get_power_batch('20200301')

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
