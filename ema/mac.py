import hmac
import hashlib
import urllib.parse

"""Message Authentication Code Generation"""

class MACGenerator:
    def __init__(self, secret_key, salt_key, salt_value, debug=False):
        self._secret_key = secret_key
        self._salt_key = salt_key
        self._salt_value = salt_value
        self._debug = debug

    def _digest(self, secret_key, msg):
        key = bytes(secret_key, 'UTF-8')
        msg_bytes = msg.encode('UTF-8')
        digester = hmac.new(key, msg_bytes, hashlib.sha1)
        return str(digester.hexdigest()).upper()

    def _build_str(self, p):
        if (self._debug):
            print('{}'.format('build_str()'))
            print('\tp={}'.format(p))
            print('\tsorted keys={}'.format(sorted(p.keys())))
        args_str = ''
        for k in sorted(p.keys()):
            args_str = args_str + k + p[k]
        url_str = urllib.parse.quote(args_str, safe='*')
        if (self._debug):
            print('\targs_str={}'.format(args_str))
            print('\turl_str={}'.format(url_str))
            print('{}'.format('build_str()'))
        return url_str

    def code(self, p):
        if (self._debug):
            print('{}'.format('code()'))
        p[self._salt_key] = self._salt_value
        url_str = self._build_str(p)
        digest = self._digest(self._secret_key, url_str)
        del p[self._salt_key]
        if (self._debug):
            print('\tdigest={}'.format(digest))
            print('{}'.format('code()'))
        return digest