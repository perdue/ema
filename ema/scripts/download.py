# -*- coding: utf-8 -*-

"""Console script for ema."""
import _localpath
import argparse
import sys
from config import parse_config
from downloader import EMADownloader
import resource_endpoints

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
    downloader = EMADownloader(
        ema_conf['host'],
        ema_conf['port'],
        ema_conf['access_token'],
        ema_conf['key'],
        conf['general'],
        args.debug)
    
    if (args.debug):
        resource_endpoints.check_endpoints(ema_conf['host'], ema_conf['port'])


#    downloader.getVersion()
    downloader.authorize(
        ema_conf['username'],
        ema_conf['password'])

    downloader.get_ecu_info()

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
