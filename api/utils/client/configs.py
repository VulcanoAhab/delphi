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

    _base_url='{host}/api/tasks_configs/

    def __init__(self):
        self._host=None
        self._job_obj={}

    def set_host(self, host):
        '''
        '''
        self._host=host

    def request(self, task_name):
        '''
        '''
        if not identifier.is_digit():
            #call by name
        else:
            #call by id
        # test response
        # load response
