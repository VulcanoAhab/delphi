import collections
import copy
import tempfile
from lxml import html

### apps imports
from information.models import PageData
from workers.models import Job
from grabbers.models import Target, ElementAction, PostElementAction, Extractor, PageAction

from grabbers.utils.confs import GrabberConf, MapperConf



## ---  find & grab page data
class Grabis:
    '''
    pagesource data interface
    for now just a simple wrappper
    '''
    @staticmethod
    def _exData(field_name, htmlElement, attrs):
        '''
        '''
        datum=[]
        for ats in attrs:
            if ats == 'text':
                datum.append(htmlElement.text)
            else:
                datum.append(htmlElement.attrib.get(ats))
        return datum

    @staticmethod
    def load_data_from_selected(elements, field, attrs):
        '''
        '''
        data_container=[dict() for _ in elements]
        for n,value in enumerate(elements):
            data=Grabis._exData(field, value, attrs)
            data_container[n].update({field:data})
        return data_container

    @staticmethod
    def load_page(browser, selector, eltype='xpath'):
        '''
        '''
        #wait for element
        browser.wait_for_element(selector, eltype=eltype)
        source=browser.get_page_source()
        return html.fromstring(source)

    def __init__(self):
        '''
        '''
        #work containers
        self._page_object=None
        self._selector=None
        #result containers
        self.data=[]
        self.page_source={}


    def set_selector(self, selector):
        '''
        '''
        self._selector=selector
        #cls.eltype=cls._geteltype(selector)
        #will be implemented soon - for now, only xptah
        self._eltype='xpath'

    def set_page_object(self, page_object):
        '''
        '''
        self._page_object=page_object

    def get_data(self, field_name, attrs={}, pure_elements=False):
        '''
        '''
        if pure_elements: return self.data
        return Grabis.load_data_from_selected(self.data, field_name, attrs)

    def grab(self):
        '''
        '''
        fn=getattr(self._page_object, self._eltype)
        self.data=fn(self._selector)

    def action(self, action_type, browser, element_index):
        '''
        '''
        els=browser.browser.find_elements_by_xpath(self._selector) #shoulb be in browser api
        getattr(els[element_index], action_type)

## ---  extract page data
class Pythoness:
    '''
    '''
    _conf={}
    _data={
        'page_source':[],
        'page_data':[],
          }

    _job=None

    @classmethod
    def set_job(cls, job):
        '''
        '''
        cls._job=job

    @classmethod
    def set_grabber(cls, grabber):
        '''
        '''
        cls._conf=GrabberConf.toDict(grabber)
        print('[+] Setting Grabber Configuration [{0}]'.format(cls._conf))

    @classmethod
    def map_sequence_targets(cls, mapper, browser):
        '''
        '''
        mapper_dict=MapperConf.toDict(mapper)
        field_name=mapper_dict['name']
        selector=mapper_dict['selector']
        page_object=Grabis.load_page(browser, selector)
        gb=Grabis()
        gb.set_selector(selector)
        gb.set_page_object(page_object)
        gb.grab()
        data=gb.get_data(field_name, pure_elements=True)
        return data


    @classmethod
    def session(cls, browser, element_index=-1):
        '''
        '''
        # set base values
        elements_lists=[]


        if 'target' in cls._conf:

            selector=cls._conf['target']['selector']
            page_object=Grabis.load_page(browser,selector)

            gb=Grabis()
            gb.set_selector(selector)
            gb.set_page_object(page_object)

            if 'element_action' in cls._conf:
                gb.action(cls._conf['element_action'],
                          browser, element_index)
            if 'extractors' in cls._conf:
                field_name=cls._conf['target']['name']
                attrs=cls._conf['extractors']
                gb.grab()
                data=gb.get_data(field_name, attrs)
                cls._data['page_data']=data

        if 'page_action' in cls._conf:
            page_action=cls._conf['page_action']
            getattr(browser, page_action)(job=cls._job)

        ### ------- last
        post_action=cls._conf['post_action']
        if post_action:
            ps=Pythoness()
            ps.set_job(cls._.job)
            ps.set_fields(post_action)
            ps.session(browser)
            ps.save_data()

    @classmethod
    def save_data(cls):
        '''
        '''
        for dict_item in cls._data['page_data']:
            print(dict_item)
#            for field_name, values in dict_item.items():
#                for value in values:
#                    if not value:continue
#                    pd=PageData()
#                    pd.field_name=field_name
#                    pd.field_value=value
#                    pd.page=page
#                    pd.save()
#


