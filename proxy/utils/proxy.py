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

    @classmethod
    def connect(cls):
        '''
        '''
        cls._server=mob.Server(cls._bin_path)
        cls._server.start()

    @classmethod
    def set_get(cls, url):
        '''
        '''
        cls._server.new_har(url)

    @classmethod
    def get_data(cls):
        '''
        '''
        return json.dumps(cls._server.har, indent=3)

    @classmethod
    def close(cls):
        '''
        '''
        cls._server.close()



