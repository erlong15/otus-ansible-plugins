from hashlib import sha1
from base64 import b64encode


class FilterModule(object):
    @staticmethod
    def _to_htpasswd(password=None):
        if not password:
            return
        res = f'new_{password}' 
        #b64encode(sha1(password.encode('utf-8')).digest())
        return res

    def filters(self):
        return {'to_htpasswd': self._to_htpasswd}

