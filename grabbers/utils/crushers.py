import collections
import copy
import tempfile
import time

from urllib.parse import urlparse

## django imports
from django.core.exceptions import ObjectDoesNotExist

### apps imports
from grabbers.utils import miners

from grabbers.utils.confs import GrabberConf, MapperConf

from information.models import PageData, make_control_key
from urlocators.models import Page, Locator, make_url_id
from workers.models import Job
from drivers.models import Header
from grabbers.models import Target, ElementAction, PostElementAction, Extractor, PageAction
from workers.utils.tasksProducer import TaskFromUrls

Grabis=miners.Grabis()

# ---  extract page & response data
#########################
class Pythoness:
    '''
    '''

    def __init__(self):
        '''
        '''
        self._conf={}
        self._job=None
        self._data={
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
            gb=Grabis
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
        #-- build page obj
        page=self._build_urllocators_objs(current_url)
        urls=[]
        for element in data:
            element_index=element['index']
            for mined_url in element[field_name]:
                if not mined_url:continue
                full_url=self._map_url(mined_url, current_url)
                urls.append(full_url)
                self._save_field(field_name, full_url, element_index, page)
        #build tasks for next crawling
        for task_config in task_configs:
            TaskFromUrls._job=self._job
            TaskFromUrls._config=task_config
            TaskFromUrls.set_urls(urls)
            TaskFromUrls.build_tasks()
        print('[+] Done creating [{}] tasks for job [{}]'.format(
                                task_configs*len(urls), self._job))

    #---- mapper helper
    ###################
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

        print("\n\n")
        print(self._conf)
        print("\n\n")

        # set base values
        if 'target' in self._conf:
            selector=self._conf['target']['selector']
            print('[+] Start targeting selector [{0}]'.format(selector))
            page_object=Grabis.load_page(self._job, browser)
            try:
                gb=Grabis
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

                if post_action:
                    pa=Pythoness()
                    pa.set_task(self._task)
                    pa.set_job(self._job)
                    pa.set_grabber(post_action)
                else:
                    pa=None

                gb.action(self._conf['element_action'], browser,
                          element_index, post_action=pa)


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
            if page_action == 'get_header_field':
                if browser_name != 'LeanRequests':
                    raise TypeError('[-] Only Lean Requests has get header field')
                #target header field is passed as extractor
                action_data.update({'header_field':self._conf['extractors']})
            elif page_action == 'execute_script':
                if browser_name == 'LeanRequests':
                    raise TypeError('[-] Lean Requests has no execute script')
                if not selector: #for now script is send by selector ---------
                    raise TypeError('[-] Script in target is required')
                field_name=field_name=self._conf['target']['name']
                action_data={'field_name':field_name, 'script':selector}
            elif page_action == 'switch_to_frame':
                if browser_name == 'LeanRequests':
                    raise TypeError('[-] Lean Requests has no execute script')
                if not selector: #for now script is send by selector ---------
                    raise TypeError('[-] Frame set_selector is required')
                field_name=field_name=self._conf['target']['name']
                action_data={'field_name':field_name, 'xpath':selector}
            print('[+] Start page action [{0}]'.format(page_action))
            getattr(browser, page_action)(page_data=self._data,
                                          action_data=action_data)



    def save_data(self, browser, target_url=None):
        '''
        '''
        url=target_url
        if not url:
            url=browser.current_url
        page=self._build_urllocators_objs(url)
        for dict_item in self._data['page_data']:
            element_index = dict_item.pop('index')
            for field_name, values in dict_item.items():
                for value in values:
                    if not value:continue
                    self._save_field(field_name, value, element_index, page)
                    time.sleep(0.001)

    def save_condition(self, browser, condition):
        '''
        '''
        condition_type = condition.save_type
        condition_confs = condition.taskconfig_set.all()
        if condition_type == 'page_data':
            msg='[-] Condition::Page Data save was'' not implemented yet'
            raise NotImplemented(msg)
        if condition_type == 'silent':return
        headers=browser.get_headers()
        print("H======>{}".format(headers))
        for k,v in headers.items():
            hea=Header()
            hea.field_name=k
            hea.field_value=v
            hea.header_name=browser._header_name
            hea.save()
            for conf in condition_confs:
                has_headers = conf.driver.headers.filter(
                    field_name=hea.field_name)
                for h_header in has_headers:
                    conf.driver.headers.remove(h_header)
                    time.sleep(0.001)
                conf.driver.headers.add(hea)
                time.sleep(0.001)

        print('[+] Done saving condition::{}'.format(condition_type))



    # --- save data  helpers
    ########################
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
        except Page.DoesNotExist:
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

    @staticmethod
    def save_proxy_data(browser):
        '''
        '''
        print(browser.get_proxy_data())
