import urllib.parse as uparse
import copy
import time
import re

from workers.models import Task, Job


#========================== / base classes \ ==========================

class UrlsOneVarPaging:
    '''
    '''
    _base_url=None
    _target_param=''
    _paging_range=[]
    _params={}
    _urls_list=[]

    @classmethod
    def set_base_url(cls, url):
        '''
        '''
        cls._base_url=url
        
    @classmethod
    def set_paging_param(cls, param_field):
        '''
        '''
        cls._target_param=param_field
        tps=[cls._target_param,]*3
        rex='{}\=\d+|{}\=|{}'.format(*tps)
        cls._target_rex=re.compile(rex, re.I)
    
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
            new_value='='.join([cls._target_param, str(param_value)])
            new_url=cls._target_rex.sub(new_value, cls._base_url)
            cls._urls_list.append(new_url)
    
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
            task=Task(target_url=url, job=cls._job, status='created') #to be aproved
            task.save()
            time.sleep(0.1)


#========================== / producer classes \ ==========================
class OneVarPagingTasks:
    '''
    '''
    
    _urls=[]
    _job_id=0
    _base_url=None
    _paging_param=None
    _paging_step=None
    _paging_range=None

    @classmethod
    def set_job_id(cls, job_id):
        '''
        '''
        cls._job_id=job_id
    
    @classmethod
    def _produce_urls(cls):
        '''
        '''
        UrlsOneVarPaging.set_base_url(cls._base_url)
        UrlsOneVarPaging.set_paging_param(cls._paging_param)
        UrlsOneVarPaging.set_paging_range(cls._paging_range[0],cls._paging_range[1],cls._paging_step)
        UrlsOneVarPaging.build_urls()
        cls._urls=UrlsOneVarPaging.get_urls()

    @classmethod
    def produce_tasks(cls, base_url, paging_param, paging_range, paging_step):
        '''
        '''
        #set urls vars and produce
        cls._base_url=base_url
        cls._paging_param=paging_param
        cls._paging_range=paging_range
        cls._paging_step=paging_step
        cls._produce_urls()
        print('[+] Done creating {} urls.'.format(len(cls._urls)))
        #produce tasks
        job=Job.objects.get(id=cls._job_id)
        TaskFromUrls.set_job(job)
        TaskFromUrls.set_urls(cls._urls)
        TaskFromUrls.build_tasks()
        print('[+] Done creatinfg tasks from urls')
