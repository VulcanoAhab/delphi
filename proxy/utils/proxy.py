import os
import json
import browsermobproxy as mob

from django.conf import settings




### ---- globals

_MOB_BIN = 'proxy/utils/browsermob-proxy/bin/browsermob-proxy'



### --- proxy classes

class MobProxy:
    '''
    '''
    _bin_path=os.path.join(settings.BASE_DIR, _MOB_BIN)
    _server=None
    _proxy=None

    @classmethod
    def connect(cls):
        '''
        '''
        cls._server=mob.Server(cls._bin_path)
        cls._server.start()
        cls._proxy = s.create_proxy()
        cls._proxy_address = "--proxy=127.0.0.1:%s" % proxy.port
    
    @classmethod
    def set_get(cls, url):
        '''
        '''
        if cls._proxy:
            cls._proxy.new_har(url)

    @classmethod
    def get_data(cls):
        '''
        '''
        if cls._proxy:
            return json.dumps(cls._proxy.har, indent=3)
        return None

    @classmethod
    def close(cls):
        '''
        '''
        if cls._server:
            cls._server.stop()
            cls._server=None


