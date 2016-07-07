import collections
import copy
import tempfile
from lxml import html

### apps imports
from grabbers.utils.confs import GrabberConf, MapperConf

from information.models import PageData
from urlocators.models import Page, Locator, make_url_id
from workers.models import Job
from grabbers.models import Target, ElementAction, PostElementAction, Extractor, PageAction




## ---  find & grab page data
class Grabis:
    '''
    pagesource data interface
    for now just a simple wrappper
    '''
    @staticmethod
    def _exData(htmlElement, attrs):
        '''
        '''
        datum=[]
        for ats in attrs:
            if ats == 'text_content':
                content=htmlElement.text
                if not content:
                    content=htmlElement.text_content()
                datum.append(content)
            elif ats == 'iframe_source':
                src=None
                for possible in ['src','data-src','href']:
                    src=htmlElement.attrib.get(possible)
                    if src:break
                datum.append(src)
            else:
                datum.append(htmlElement.attrib.get(ats))
        return datum

    @staticmethod
    def load_data_from_selected(elements, field, attrs):
        '''
        '''
        data_container=[dict() for _ in elements]
        for n,value in enumerate(elements):
            data=Grabis._exData(value, attrs)
            data_container[n].update({field:data})
        return data_container

    @staticmethod
    def load_page(browser, selector, eltype='xpath'):
        '''
        '''
        #wait for element
        try:
            browser.wait_for_element(selector, eltype=eltype)
        except:
            return None
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
        if page_object is None:
            raise Exception('[-] Fail to load page_object')
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

    def action(self, action_type, browser, element_index,
                                post_action=None, job=None):
        '''
        '''
        els=browser.browser.find_elements_by_xpath(self._selector) #shoulb be in browser api
        if element_index >=0:
            targets=[els[element_index]]
        else:
            targets=els
        for target in targets:
            getattr(target, action_type)()
            if post_action:
                if not job:
                    raise Exception('[-] Jobs is required for post action')
                ps=Pythoness()
                ps.set_job(job)
                ps.set_grabber(post_action)
                ps.session(browser)
                ps.save_data()

## ---  extract page data
class Pythoness:
    '''
    '''
    _job=None

    @classmethod
    def set_job(cls, job):
        '''
        '''
        cls._job=job

    def __init__(self):
        '''
        '''
        self._conf={}
        self._data={
            'page_source':[],
            'page_data':[],
                    }
    def set_grabber(self, grabber):
        '''
        '''
        self._conf=GrabberConf.toDict(grabber)
        print('[+] Setting Grabber Configuration')

    def map_sequence_targets(self, mapper, browser):
        '''
        '''
        mapper_dict=MapperConf.toDict(mapper)
        field_name=mapper_dict['name']
        selector=mapper_dict['selector']
        page_object=Grabis.load_page(browser, selector)
        try:
            gb=Grabis()
            gb.set_selector(selector)
            gb.set_page_object(page_object)
            gb.grab()
            data=gb.get_data(field_name, pure_elements=True)
            return data
        except Exception as e:
            print('[-] Fail to build map', e)
            return []

    def session(self, browser, element_index=-1):
        '''
        '''
        # set base values
        if 'target' in self._conf:
            selector=self._conf['target']['selector']
            print('[+] Start mining with selector [{0}]'.format(selector))
            page_object=Grabis.load_page(browser,selector)
            try:
                gb=Grabis()
                gb.set_selector(selector)
                gb.set_page_object(page_object)
            except Exception as e:
                print('[-] Fail to load conf in Grabis', e)
                return
            if 'element_action' in self._conf:
                post_action=self._conf['post_action']
                gb.action(self._conf['element_action'], browser,
                          element_index, post_action=post_action,
                          job=self._job)
            if 'extractors' in self._conf:
                field_name=self._conf['target']['name']
                attrs=self._conf['extractors']
                gb.grab()
                data=gb.get_data(field_name, attrs)
                self._data['page_data']=data
        if 'page_action' in self._conf:
            page_action=self._conf['page_action']
            print('[+] Start page action [{0}]'.format(page_action))
            getattr(browser, page_action)(job=self._job)


    def save_data(self, browser):
        '''
        '''
        url=browser.current_url
        url_id=make_url_id(url)
        for dict_item in self._data['page_data']:
            for field_name, values in dict_item.items():
                for value in values:
                    if not value:continue
                    pd=PageData()
                    pd.field_name=field_name
                    pd.field_value=value
                    pd.page=page
                    pd.save()



