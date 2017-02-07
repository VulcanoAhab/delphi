import requests
from api.utils.client.models import *

class TaskConfig:
    '''
    '''
    _base="http://{host}:{port}/api/tasks_configs/{config_name}/?format=json"
    HOST=None
    PORT=None

    @classmethod
    def set_host(cls, host="127.0.0.1"):
        '''
        '''
        cls.HOST=host

    @classmethod
    def set_port(cls, port=9097):
        '''
        '''
        cls.PORT=port

    def __init__(self, config_name):
        '''
        '''
        self.response=None
        self.configuration_name=config_name
        if self.HOST is None:self.set_host()
        if self.PORT is None:self.set_port()
        self.url=self._base.format(
            host=self.HOST,
            port=self.PORT,
            config_name=self.configuration_name
        )

    def fetch(self):
        '''
        '''
        response=requests.get(self.url)
        response.raise_for_status()
        self.response=response.json()


    @proterty
    def toJsonFile(self, file_name):
        '''
        '''
        return self.response


    # def load(self):
    #     '''
    #     '''
    #     self.driver=Driver(**self.response['driver'])
    #     self.sequences=[Sequence(**s) for k,s in self.response['sequence'].items()]
    #     self.mapper=Mapper(**self.response['mapper'])
    #     self.round_limit=self.response['round_limit']
