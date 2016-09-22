import collections
import copy
import tempfile
from lxml import html
from lxml import etree
from urllib.parse import urlparse

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
                estr=etree._ElementUnicodeResult #just insurance
                if isinstance(htmlElement, (str,estr)):
                    content=htmlElement.strip()
                else:
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
    def load_page(job, browser, save_source=True):
        '''
        '''
        #save page source
        if save_source:
            browser.page_source(job=job)
        #get and return page source
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
        returns
        ------
        list: [{field_name:field_data, index:element_index},...]
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

    def set_task(self, task):
        '''
        '''
        self._task=task


    def set_grabber(self, grabber):
        '''
        '''
        self._conf=GrabberConf.toDict(grabber)
        print('[+] Setting Grabber Configuration')

    def map_targets(self, mapper, browser):
        '''
        action
        ------
        maps urls on target pages
        creates tasks with diferent taskconfigs
        save url with field name on information db

        obs
        ---
        this guy here is an hybric fellow
        so he is kind out place here...
        '''
        #set vars
        field_name=mapper.field_name
        print('[+] Starting Mapper [{}]'.format(field_name))
        selector=mapper.field_selector
        task_configs=TaskConfig.objects.filter(mapper=mapper)
        page_object=Grabis.load_page(self._job, browser, save_source=False)
        #mine target links
        try:
            gb=Grabis()
            gb.set_selector(selector)
            gb.set_page_object(page_object)
            gb.grab()
            #mapper element attr is always generic link
            data=gb.get_data(field_name, ['generic_link',])
        except Exception as e:
            print('[-] Fail to extract link in mapper: [{}]'.format(e))
            return
        #create mapper tasks
        current_url = urlparse(browser.current_url)
        #--save page source
        page=browser.page_source(job=self._job, return_page=True)
        urls=[]
        for element in data:
            element_index=element['index']
            for mined_url in element[field_name]:
                if not mined_url:continue
                full_url=self._map_url(mined_url, current_url)
                urls.append(full_url)
                self._save_field(field_name, full_url, element_index, page)
        for task_config in task_configs:
            TaskFromUrls._job=self._job
            TaskFromUrls._config=task_config
            TaskFromUrls.set_urls(urls)
            TaskFromUrls.build_tasks()
        print('[+] Done creating [{}] tasks for job [{}]'.format(
                                task_configs*len(urls), self._job))

    #---- mapper helper
    def _map_url(self, u, current_url):
        parsed_url = urlparse(u)
        if not parsed_url.netloc:
            parsed_url = parsed_url._replace(
                netloc=current_url.netloc.lower(),
                scheme=current_url.scheme)
        return parsed_url.geturl()

    def session(self, browser, element_index=-1):
        '''
        '''
        #get general vals
        browser_name=browser.__class__.__name__
        # set base values
        if 'target' in self._conf:
            selector=self._conf['target']['selector']
            print('[+] Start targeting selector [{0}]'.format(selector))
            page_object=Grabis.load_page(self._job, browser)
            try:
                gb=Grabis()
                gb.set_selector(selector)
                gb.set_page_object(page_object)
            except Exception as e:
                print('[-] Fail to load conf in Grabis', e)
                return
            if 'element_action' in self._conf:
                #test browser type
                if browser_name == 'LeanRequests':
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
            action_data={}
            #legacy - now is required
            if page_action == 'page_source':return
            if page_action == 'get_header_field':
                if browser_name != 'LeanRequests':
                    raise TypeError('[-] Only Lean Requests has get header field')
                #target header field is passed as extractor
                action_data.update({'header_field':self._conf['extractors']})
            if page_action == 'execute_script':
                if browser_name == 'LeanRequests':
                    raise TypeError('[-] Lean Requests has no execute script')
                if not selector: #for now script is send by selector ---------
                    raise TypeError('[-] Script in target is required')
                field_name=field_name=self._conf['target']['name']
                action_data={'field_name':field_name, 'script':selector}
            print('[+] Start page action [{0}]'.format(page_action))
            getattr(browser, page_action)(page_data=self._data,
                                          action_data=action_data)


    def save_data(self, browser):
        '''
        '''
        url=browser.current_url
        page=self._build_urllocators_objs(url)
        for dict_item in self._data['page_data']:
            element_index = dict_item.pop('index')
            for field_name, values in dict_item.items():
                for value in values:
                    if not value:continue
                    self._save_field(field_name, value, element_index, page)

    # --- save data  helpers
    def _build_urllocators_objs(self, url):
        '''
        obs
        ---------
        this function is very similar
        to save page source in browser
        the only difference is html source persistence

        *** soon will merge both ****
        '''
        #build url relations
        url_id=make_url_id(url)
        try:
            locs=Locator.objects.get(url_id=url_id)
        except ObjectDoesNotExist:
            locs=Locator()
            locs.url=url
            locs.save()
        #build page relation
        try:
            page=Page.objects.get(addr=locs.id, job=self._job)
        except ObjectDoesNotExist:
            page=Page()
            page.job=self._job
            page.task=self._task
            page.addr=locs
            page.save()
        return page

    def _save_field(self, field_name, value, element_index, page):
        '''
        '''
        control_key=make_control_key(field_name, value, page.id)
        is_duplicate=PageData.objects.filter(control_key=control_key)
        if is_duplicate.count():return
        pd=PageData()
        pd.field_name=field_name
        pd.field_value=value
        pd.element_index = element_index
        pd.page=page
        pd.job=self._job
        pd.task=self._task
        pd.save()

    @classmethod
    def save_proxy_data(cls, browser):
        '''
        '''
        print('Called ----------- save proxy data')
        print(browser.get_proxy_data())
