import urllib.parse as uparse
import copy
import time


from workers.models import Task


class UrlsFromPaging:
    '''
    '''
    _base_url_list=[]
    _target_param=''
    _paging_range=[]
    _params={}
    _urls_list=[]

    @classmethod
    def load_sample_url(cls, url):
        '''
        '''
        cls._base_url_list=list(uparse.urlparse(url))
        cls._params=dict(uparse.parse_qsl(cls._base_url_list[4]))
        
    @classmethod
    def set_paging_param(cls, param_field):
        '''
        '''
        cls._target_param=param_field

    @classmethod
    def set_paging_range(cls, start_value, max_value, step_size=1):
        '''
        '''
        cls._paging_range=list(range(start_value, max_value, step_size))

    @classmethod
    def build_urls(cls):
        '''
        '''
        for param_value in cls._paging_range:
            new_params=copy.deepcopy(cls._params)
            new_params[cls._target_param]=param_value
            new_url=copy.deepcopy(cls._base_url_list)
            new_url[4]=new_params
            cls._urls_list.append(uparse.urlunparse(new_url))
    
    @classmethod
    def get_urls(cls):
        '''
        '''
        return cls._urls_list


class TaskFromUrls:
    '''
    '''

    @classmethod
    def set_job(cls, job):
        '''
        '''
        cls._job=job
    
    @classmethod
    def set_urls(cls, urls):
        '''
        '''
        cls._urls=urls

    @classmethod
    def build_tasks(cls):
        '''
        '''
        for url in cls._urls:
            task=Task(target_url=url, job=cls._job, status='to_approve') #to be aproved
            task.save()
            time.sleep(0.1)
