import collections
import copy
import tempfile
from lxml import html

## django imports
from django.core.exceptions import ObjectDoesNotExist

### apps imports
from grabbers.utils.confs import GrabberConf, MapperConf

from information.models import PageData, make_control_key
from urlocators.models import Page, Locator, make_url_id
from workers.models import Job
from grabbers.models import Target, ElementAction, PostElementAction, Extractor, PageAction
from workers.utils.tasksProducer import TaskFromUrls



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
                if not content or not content.strip():
                    content=htmlElement.text_content()
                datum.append(content)
            elif ats == 'generic_link':
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
            data_container[n].update({field:data, 'index': n})
        return data_container

    @staticmethod
    def load_page(browser):
        '''
        '''
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

    def get_data(self, field_name, attrs=[], as_elements=False):
        '''
        '''
        if as_elements: return self.data
        return Grabis.load_data_from_selected(self.data, field_name, attrs)

    def grab(self):
        '''
        '''
        fn=getattr(self._page_object, self._eltype)
        try:
            self.data=fn(self._selector)
        except Exception as e:
            print('[+] Fail to find element', self._selector)
            return 2

    def action(self, action_type, browser, element_index,
                                post_action=None, job=None):
        '''
        '''
        try:
            els=browser.browser.find_elements_by_xpath(self._selector) #shoulb be in browser api
        except Exception as e:
            print('[+] Fail to find element', self._selector)
            return 2
        if element_index >=0:
            elslen=len(els)
            if element_index > elslen-1:
                print('[-] Index out of range GOT: [{}] | LEN [{}]'.format(element_index, elslen))
                return 1
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
                ps.save_data(browser)

## ---  extract page data
class Pythoness:
    '''
    '''

    def __init__(self):
        '''
        '''
        self._conf={}
        self._job=None
        self._data={
            'page_source':[],
            'page_data':[],
                    }

    def set_job(self, job):
        '''
        '''
        self._job=job

    def set_grabber(self, grabber):
        '''
        '''
        self._conf=GrabberConf.toDict(grabber)
        print('[+] Setting Grabber Configuration')

    def map_targets(self, mapper, browser):
        '''
        '''
        #set vars
        field_name=mapper.field_name
        print('[+] Starting Mapper [{}]'.format(field_name))
        selector=mapper.field_selector
        task_config=mapper.task_config
        page_object=Grabis.load_page(browser)
        #mine target links
        try:
            gb=Grabis()
            gb.set_selector(selector)
            gb.set_page_object(page_object)
            gb.grab()
            data=gb.get_data(field_name, ['generic_link',])
        except Exception as e:
            print('[-] Fail to extract link in mapper', e)
            return
        #create mapper tasks
        urls=[d for e in data for d in e[field_name] if d]
        TaskFromUrls._job=self._job
        TaskFromUrls._config=task_config
        TaskFromUrls.set_urls(urls)
        TaskFromUrls.build_tasks()
        print('[+] Done creating tasks')


    def session(self, browser, element_index=-1):
        '''
        '''
        # set base values
        if 'target' in self._conf:
            selector=self._conf['target']['selector']
            print('[+] Start mining with selector [{0}]'.format(selector))
            page_object=Grabis.load_page(browser)
            try:
                gb=Grabis()
                gb.set_selector(selector)
                gb.set_page_object(page_object)
            except Exception as e:
                print('=====', e)
                print('[-] Fail to load conf in Grabis', e)
                return
            if 'element_action' in self._conf:
                #test browser type
                if browser.__class__.__name__ == 'LeanRequests':
                    raise TypeError('[-] Lean Requests has no action')
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
            #it's dirty - needs to improve
            page_action=self._conf['page_action']
            field_name=None
            if 'extractors' in self._conf:
                field_name=self._conf['extractors']
            print('[+] Start page action [{0}]'.format(page_action))
            getattr(browser, page_action)(job=self._job,
                                          page_data=self._data,
                                          header_field=field_name)


    def save_data(self, browser):
        '''
        '''
        url=browser.current_url
        url_id=make_url_id(url)
        #build url relations
        try:
            locs=Locator.objects.get(url_id=url_id)
        except ObjectDoesNotExist:
            locs=Locator()
            locs.url=url
            locs.save()

        try:
            page=Page.objects.get(addr=locs.id)
        except ObjectDoesNotExist:
            page=Page()
            #build html file
            page.job=self._job
            page.addr=locs
            page.save()
            #close temp file

        for dict_item in self._data['page_data']:
            element_index = dict_item.pop('index')
            for field_name, values in dict_item.items():
                for value in values:
                    if not value:continue
                    control_key=make_control_key(field_name, value, page.id)
                    is_duplicate=PageData.objects.filter(control_key=control_key)
                    if is_duplicate.count():continue
                    pd=PageData()
                    pd.field_name=field_name
                    pd.field_value=value
                    pd.element_index = element_index
                    pd.page=page
                    pd.save()



