# -*- coding: utf-8 -*-

"""Console script for ema."""
import _localpath
import argparse
import sys
from config import parse_config
from ema import EMA
import resource_endpoints

def main():
    """Console script for ema."""

    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')

    required.add_argument(
        "-c", "--conf", required=True, action="store",
        dest="yaml_file",
        help="Path to YAML config file"
    )
    args = parser.parse_args()

    conf = parse_config(path=args.yaml_file)

    print("Using config file: " +
          str(args.yaml_file))

    ema_conf = conf['ema']
    ema = EMA(ema_conf['host'],
              ema_conf['port'],
              ema_conf['key'],
              conf['general'])
    
    resource_endpoints.check_endpoints(ema_conf['host'], ema_conf['port'])


#    ema.getVersion()
    ema.authorize(
        ema_conf['access_token'],
        ema_conf['username'],
        ema_conf['password'],
        ema_conf['checkcode'])
#    ema.login(ema_conf['username'],
#              ema_conf['password'])

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
