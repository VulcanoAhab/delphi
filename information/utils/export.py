from django.core import serializers
from django.conf import settings
import os
import itertools
import json

from information.models import PageData
from urlocators.models import Page
from workers.models import Job


class Pull:
    '''
    '''

    @classmethod
    def set_job_id(cls, job_id):
        '''
        '''
        cls._job_id=job_id

    @classmethod
    def data_per_job(cls, fields_name=[]):
        '''
        '''
        pages_data=[]
        pages=Page.objects.filter(job=cls._job_id)
        for page in pages:
            page_data=PageData.objects.filter(page=page)
            if fields_name:
                page_data=page_data.filter(field_name__in=fields_name)
            if not page_data or page_data.count()==0:continue
            pages_data.append(page_data)
        return pages_data

    @classmethod
    def data_per_urls(cls, seed_urls, chain_fields, data_fields):
        '''
        params
        ------
        seed_urls: the query roots urls
        urls_chain: target_fields name [that hold urls chain]
        values_field_name:fields name from the target values

        '''
        pages_data=[]
        for seed in seed_urls:
            page=Page.objects.get(addr__url=seed)
            page_data=PageData.objects.filter(page=page)
            page_dict={
                'seed':seed,
                'page_data':page_data,
                'index':0,
                'chain_fields':chain_fields,
                'data_fields':data_fields,
                    }
            pages_data.append(page_dict)
        return pages_data


class JsonPage:
    '''
    '''

    _base=[]
    _file_name=''
    _pages_json=[]
    _job_name=[]
    _to='file' #or redis

    @classmethod
    def set_export_format(cls, to):
        '''
        '''
        cls._to=to

    @classmethod
    def _file(cls):
        '''
        '''
        job_path=os.path.join(settings.DATA_ROOT, cls._job_name)
        if not os.path.exists(job_path):os.makedirs(job_path)
        file_path=os.path.join(job_path, cls._file_name)
        fd=open(file_path, 'w')
        json.dump(cls._pages_json, fd)
        fd.close()

    @classmethod
    def _export(cls):
        '''
        '''
        if cls._to == 'file':
            cls._file()
            print('[=[<o>]=] Done saving file: {} [=[<o>]=]'.format(cls._file_name))
        elif cls._to == 'api':
            raise NotImplemented('[-] EXPORT FORMAT TO BE IMPLEMENTED')
        else:
            raise TypeError('[-] Unkown export format')

    @classmethod
    def set_data(cls, base_data):
        '''
        '''
        cls._base=base_data

    @classmethod
    def set_job_name(cls, job_name):
        '''
        '''
        cls._job_name=job_name

    @classmethod
    def by_job(cls, file_name, fields_name=[]):
        '''
        '''
        cls._pages_json=[]
        cls._file_name=file_name
        for page_data in cls._base:
            if target_fields_name:
                page={r.fields_name:r.field_value
                      for r in page_data
                      if r.fild_name in fields_name}
            else:
                 page={r.field_name:r.field_value
                       for r in page_data}
            cls._pages_json.append(page)
        cls._export()


    @classmethod
    def by_urls_chain(cls, file_name):
        '''
        '''
        cls._file_name=file_name
        cls._pages_json=cls._urls_chain(cls._base)
        cls._export()


    @classmethod
    def _urls_chain(cls, page_dict_list, chain_container=None):
        '''
        '''

        pages_list=[]
        for page_dict in page_dict_list:

            url=page_dict['seed']
            page_data=page_dict.pop('page_data')
            index=page_dict['index']
            chain_fields=page_dict.pop('chain_fields')
            data_fields=page_dict.pop('data_fields')
            chain_size=len(chain_fields)
            next_index=index+1

            #if it is first iteraction
            if chain_container is None:
                #this guy will a class soon - for now repetition
                page_chain={
                    'seed':url,
                    'index':index,
                    'nodes':[],
                    'data':[],
                    'chain_fields':chain_fields,
                    'data_fields':data_fields,
                        }
                container=page_chain['nodes']
                #add page chain dict to final chain result list
                pages_list.append(page_chain)
            else:
                container=chain_container

            #if is final chain field -> target data field
            if index >= chain_size:
                final_data=page_data.filter(field_name__in=data_fields)
                final_data=[{p.field_name:p.field_value}
                            for p in final_data]
                final_chain={
                    'seed':url,
                    'index':next_index,
                    'values':final_data,
                        }
                container.append(final_chain)
                continue

            #building chain
            chain_field=chain_fields[index]
            next_datum=page_data.filter(field_name=chain_field)
            next_dicts=[]
            for next_data in next_datum:
                next_url=next_data.field_value
                next_page=Page.objects.get(addr__url__contains=next_url)
                next_page_data=PageData.objects.filter(page=next_page)
                next_chain={'seed':next_url,
                           'page_data':next_page_data,
                           'index':next_index,
                           'chain_fields':chain_fields,
                           'data_fields':data_fields,
                           'nodes':[],
                           'data':[]}
                if next_index >= chain_size:
                    next_container=next_chain['data']
                else:
                    next_container=next_chain['nodes']
                container.append(next_chain)
                cls._urls_chain([next_chain], next_container)

        return pages_list

class Export:
    '''
    '''

    @classmethod
    def job_to_json(cls, job_id, file_name, fields_name=[]):
        '''
        '''
        job=Job.objects.get(id=job_id)
        Pull.set_job_id=job_id
        data=Pull.data_per_job(fields_name)
        JsonPage.set_job_name(job.name)
        JsonPage.set_data(data)
        JsonPage.by_job(file_name)


    @classmethod
    def urlsChain_to_json(cls, job_id, file_name, urls, chain_fields, data_fields):
        '''
        '''
        if not file_name.endswith('.json'):
            file_name='.'.join([file_name, 'json'])
        job=Job.objects.get(id=job_id)
        data=Pull.data_per_urls(urls, chain_fields, data_fields)
        JsonPage.set_job_name(job.name)
        JsonPage.set_data(data)
        #testing
        JsonPage.by_urls_chain(file_name)



