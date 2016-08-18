from information.models import PageData
from urlocators.models import Page
from django.core import serializers
from django.conf import settings
import os
import itertools
import json

class Pull:
    '''
    '''

    @classmethod
    def data_per_job(cls, job_id, fields_name=[]):
        '''
        '''
        pages_data=[]
        pages=Page.objects.filter(job=job_id)
        for page in pages:
            page_data=PageData.objects.filter(page=page)
            if fields_name:
                page_data=page_data.filter(field_name__in=fields_name)
            if not page_data or page_data.count()==0:continue
            pages_data.append(page_data)
        return pages_data


class Save:
    '''
    '''
    
    _queries=[]

    @classmethod
    def set_query_list(cls, query_list):
        '''
        '''
        cls._queries=query_list
        
    @classmethod
    def as_json(cls, file_name):
        '''
        '''
        pages_json=[]
        for page_data in cls._queries:
                page={r.field_name:r.field_value for r in page_data}
                pages_json.append(page)
        file_path=os.path.join(settings.DATA_ROOT,file_name)
        fd=open(file_path, 'w')
        json.dump(pages_json, fd)
        fd.close()
        print('[=[<o>]=] Done saving file: {} [=[<o>]=]'.format(file_name))

class Export:
    '''
    '''
    
    @classmethod
    def job_to_json(cls, job_id, file_name):
        '''
        '''
        data=Pull.data_per_job(job_id)
        Save.set_query_list(data)
        Save.as_json(file_name)
