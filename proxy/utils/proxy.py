import os
import json
import browsermobproxy as mob

from django.conf import settings
from proxy.models import Entry



### ---- globals

_MOB_BIN = 'proxy/utils/browsermob-proxy/bin/browsermob-proxy'



### --- proxy classes

class MobProxy:
    '''
    '''
    _bin_path=os.path.join(settings.BASE_DIR, _MOB_BIN)
    _server=None
    _proxy=None
    _target_url=None

    @classmethod
    def connect(cls, task):
        '''
        '''
        proxy_obj=task.config.proxy
        if not proxy_obj:return
        if proxy_obj.status == 'off':
            raise SystemError('[-] Proxy is set but server is off')
        har_id=task.job.id
        cls._target_url=task.target_url
        cls._server=mob.Server(cls._bin_path)
        cls._server.start()
        cls._proxy = cls._server.create_proxy()
        cls._proxy.new_har(har_id)

    @classmethod
    def get_data(cls):
        '''
        '''
        if not cls._proxy:return
        return MobProxy.proxy_response(cls._proxy.har)


    @classmethod
    def save_data(cls):
        '''
        '''
        if not cls._proxy:return
        entries=cls._proxy.har['log']['entries']
        if not entries:return
        for entry in entries:
            modeled_entry=cls._extract(entry)
            db_entry=Entry(**modeled_entry)
            db_entry.save()

    @classmethod
    def port(cls):
        '''
        '''
        if not cls._proxy:return
        return cls._proxy.port

    @classmethod
    def close(cls):
        '''
        '''
        if not cls._server:return
        cls._server.stop()
        cls._server=None

    @classmethod
    def proxy_response(cls, har_obj):
        '''
        '''
        entries=har_obj['log']['entries']
        if not entries:return
        parsed_list=[cls._extract(e) for e in entries if e]
        return parsed_list

    @classmethod
    def _extract(cls, entry):
        '''
        '''
        if not entry:return
        #request data
        request=entry['request']
        url=request['url']
        method=request['method']
        #control data
        dest_ip=entry['serverIPAddress']
        job_id=entry['pageref']
        duration=entry['time']
        #response data
        response=entry['response']
        content_type=response['content']['mimeType']
        entry_dict={
            'url':url,
            'method':method,
            'dest_ip':dest_ip,
            'job_id':job_id,
            'duration':duration,
            'content_type':content_type,
            'target_url':cls._target_url,
                }
        return entry_dict


