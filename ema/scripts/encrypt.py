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
        "-a", "--access_token", required=True, action="store",
        dest="access_token",
        help="EMA app identifier"
    )
    required.add_argument(
        "-s", "--secret_key", required=True, action="store",
        dest="secret_key",
        help="EMA app hash secret key"
    )
    required.add_argument(
        "-sk", "--salt_key", required=True, action="store",
        dest="salt_key",
        help="EMA app hash salt key"
    )
    required.add_argument(
        "-sv", "--salt_value", required=True, action="store",
        dest="salt_value",
        help="EMA app hash salt value"
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

    access_token, secret_key, salt_key, salt_value, username, password, key = crypt.generate(args.access_token, args.secret_key, args.salt_key, args.salt_value, args.username, args.password, args.key)
    crypt.write_credentials(access_token, secret_key, salt_key, salt_value, username, password, args.outfile)

    if key != args.key:
        crypt.write_key(key, args.keyfile)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
