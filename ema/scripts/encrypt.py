# -*- coding: utf-8 -*-

"""Console script for encryption of credentials."""
import _localpath
import argparse
import sys
import crypt
import os

def main():
    """Console script for encryption of credentials."""
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')

    required.add_argument(
        "-a", "--appid", required=True, action="store",
        dest="appid",
        help="EMA app identifier"
    )
    required.add_argument(
        "-u", "--username", required=True, action="store",
        dest="username",
        help="EMA username"
    )
    required.add_argument(
        "-p", "--password", required=True, action="store",
        dest="password",
        help="EMA password"
    )
    optional.add_argument(
        "-k", "--key", required=False, action="store",
        dest="key",
        help="encryption key"
    )
    optional.add_argument(
        "-K", "--key-filename", required=False, action="store",
        dest="keyfile",
        help="file to store key [default = ~/.ema/key]",
        default=os.path.expanduser("~")+"/.ema/key"
    )
    optional.add_argument(
        "-C", "--credentials-filename", required=False, action="store",
        dest="outfile",
        help="file to store credentials [default = ~/.ema/credentials]",
        default=os.path.expanduser("~")+"/.ema/credentials"
    )
    parser._action_groups.append(optional)
    args = parser.parse_args()
    if args.key is not None:
        args.key = str.encode(args.key)

    key, appid, username, password = crypt.generate(args.appid, args.username, args.password, args.key)
    crypt.write_key(key, args.keyfile)
    crypt.write_credentials(appid, username, password, args.outfile)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
