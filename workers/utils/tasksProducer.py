import functools
import urllib.parse as uparse
import copy
import time
import re

from workers.models import Task, Job, TaskConfig
from information.models import PageData

#========================== / base classes \ ==========================
# under construction -- still designing patterns

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
        if url.endswith('/'):
            url = url[:-1]
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
        cls._paging_range=list(range(start_value, max_value+1, step_size))

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


class UrlsOneVarPath(UrlsOneVarPaging):
    '''
    '''

    @classmethod
    def set_paging_range(cls, start_value, max_value, step_size=1):
        if start_value.isalpha() and max_value.isalpha():
            start_value = ord(start_value)
            max_value = ord(max_value)

        super(UrlsOneVarPath, cls).set_paging_range(
            start_value, max_value, step_size)

    @classmethod
    def build_urls(cls, ascii=False):
        for param_value in cls._paging_range:
            if ascii:
                param_value = chr(param_value)
            new_url = '{}/{}'.format(cls._base_url, param_value)
            cls._urls_list.append(new_url)


class TaskFromResults:
    '''
    '''
    _target_job=None
    _target_query=None
    _target_urls=[]

    @classmethod
    def set_job(cls, job_id):
        '''
        '''
        cls._target_job=job_id

    @classmethod
    def pull_results(cls):
        '''
        '''
        cls._target_query=PageData.objects.filter(page__job=cls._target_job)


    @classmethod
    def process_results(cls, process_function):
        '''
        '''
        cls._target_urls=process_function(cls._target_query)

    @classmethod
    def get_urls(cls):
        '''
        '''
        return cls._target_urls


class TaskFromUrls:
    '''
    '''

    @classmethod
    def set_job(cls, job_pointer):
        '''
        '''
        if isinstance(job_pointer, Job):
            cls._job=job_pointer
        else:
            try:
                job_id=int(job_pointer)
            except:
                raise TypeError('[+] [{}] Unkown job pointer.'.format(cls.__class__.name))
            cls._job=Job.objects.get(id=job_id)

    @classmethod
    def set_urls(cls, urls):
        '''
        '''
        cls._urls=urls

    @classmethod
    def set_config_name(cls, config_name):
        '''
        '''
        cls._config_name=config_name
        cls._config=TaskConfig.objects.get(name=config_name)

    @classmethod
    def build_tasks(cls):
        '''
        '''
        for url in cls._urls:
            #test if task with the same url already exists inside same job
            task_in=Task.objects.filter(job=cls._job, target_url=url).first()
            if task_in:continue
            task=Task(  target_url=url,
                        job=cls._job,
                        status='created',# ? to be approved ?
                        config=cls._config)
            task.save()
            time.sleep(0.001)


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
    def set_config_name(cls, config_name):
        '''
        '''
        cls._config_name=config_name


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
        TaskFromUrls.set_job(cls._job_id)
        TaskFromUrls.set_config_name(cls._config_name)
        TaskFromUrls.set_urls(cls._urls)
        TaskFromUrls.build_tasks()
        print('[+] Done creatinfg tasks from urls')


class ResultsTasks:
    '''
    '''
    _tasks_job=None
    _results_job=None

    @staticmethod
    def tasks_by_field(field):
        '''
        '''
        def extract_values(field, target_query):
            '''
            '''
            query=target_query.filter(field_name=field)
            print('[+] Query for field {} has {} results'.format(field,query.count()))
            return [r.field_value for r in query]
        return functools.partial(extract_values, field)

    @classmethod
    def set_tasks_job(cls, job_id):
        '''
        '''
        cls._tasks_job=job_id

    @classmethod
    def set_results_job(cls, job_id):
        '''
        '''
        cls._results_job=job_id

    @classmethod
    def set_config_name(cls, config_name):
        '''
        '''
        cls._config_name=config_name

    @classmethod
    def produce_tasks(cls, producer_fn):
        '''
        '''
        TaskFromResults.set_job(cls._results_job)
        TaskFromResults.pull_results()
        TaskFromResults.process_results(producer_fn)
        task_urls=TaskFromResults.get_urls()
        print('[+] Done mining {} target urls'.format(len(task_urls)))
        TaskFromUrls.set_job(cls._tasks_job)
        TaskFromUrls.set_urls(task_urls)
        TaskFromUrls.set_config_name(config_name)
        TaskFromUrls.build_tasks()
        print('[+] Done building tasks...')


