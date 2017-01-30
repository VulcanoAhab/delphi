import requests


class Config:
    '''
    '''
    def __init__(self):
        '''
        '''
        pass

class Fetch:
    '''
    '''

    _endpoint='/api/tasks_configs/{name}'

    def __init__(self, HOST):
        self._host=HOST
        self._job_obj={}
        self._target_url=None

    def set_host(self, host):
        '''
        '''
        self._host=host

    def name(self, task_name):
        '''
        '''
        _target=self._name_endpoint.format(task_name)
        self._target_url=self._host+_target

    def load(self):
        '''
        '''
        r=requests.get(self._target_url)
        r.raise_for_status()
        self._job_obj=r.json()




class Save:
    '''
    '''

    def __init__(self):
        '''
        '''
        pass
