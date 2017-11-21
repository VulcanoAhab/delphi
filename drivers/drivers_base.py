import tempfile
import requests
import os
import signal
import json
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#django
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

#db models
from urlocators.models import Page, Locator, make_url_id
#===========================================================#
#=================== Drivers helpers =======================#
class Helpers:
    '''
    '''
    @staticmethod
    def _save_headers(headers, header_name):
        '''
        '''
        pass

    @staticmethod
    def _page_to_file_or_db(source, locs, job, page_to):
        '''
        '''
        page=Page()
        #build html file
        page.job=job
        page.addr=locs
        # ---  options are not impleted on model level yet
        page_to='db'
        # ---
        #persiste
        if page_to == 'db':
            page.html=source
            page.save()
        elif page_to == 'filesystem':
            fp=tempfile.TemporaryFile()
            fp.write(source.encode())
            fp.seek(0)
            file_html=File(fp)
            page.html=source
            page.save()
            fp.close()

    @staticmethod
    def save_page_source(url, source, page_to='db', **kwargs):
        '''
        '''
        #set url id
        url_id=make_url_id(url)
        #get job
        try:
            job=kwargs['job']
        except KeyError:
            raise Exception('[-] Job is required to save page source')
        #build url relations
        try:
            locs=Locator.objects.get(url_id=url_id)
        except ObjectDoesNotExist:
            locs=Locator()
            locs.url=url
            locs.save()
        try:
            page=Page.objects.get(addr=locs.id, job=job)
        except ObjectDoesNotExist:
            Helpers._page_to_file_or_db(source, locs, job, page_to)
        print('[+] Done saving page [{}]'.format(url[:150]))
        if ('return_page' in kwargs):return page

    @staticmethod
    def save_screenshot(url, screenshot, **kwargs):
        '''
        '''
        #set url id
        url_id=make_url_id(url)
        #get job
        try:
            job=kwargs['job']
        except KeyError:
            raise Exception('[-] Job is required to save page source')
        #build url relations
        try:
            locs=Locator.objects.get(url_id=url_id)
        except ObjectDoesNotExist:
            locs=Locator()
            locs.url=url
            locs.save()
        #build and save page
        page=Page.objects.get_or_create(addr=locs.id, job=job)
        page.screenshot=screenshot

#===========================================================#
#==================== Drivers base classes =================#
class BaseSeleniumBrowser:
    '''
    '''
    def __init__(self, driver_name, **kwargs):
        '''
        '''
        self._driver_name=driver_name
        self._driver=webdriver
        self.host=''
        self.pid=None
        self.browser=None
        self.proxy=None
        self.kwargs=kwargs

    def set_host(self, host):
        '''
        '''
        self.host=host

    def load_confs(self, confObject):
        '''
        '''
        raise NotImplemented('Need to implemented at browser level')

    def build_driver(self, taskConfs=None, proxy_port=None):
        '''
        '''
        #set browser global waits
        max_implicity=5
        max_timeout=30
        #defaults
        if "service_args" not in  self.kwargs:
            self.kwargs["service_args"]=["--ignore-ssl-errors=yes"]
        if proxy_port:
            proxy_addr="--proxy=127.0.0.1:{}".format(proxy_port)
            service_args=[proxy_addr,]
            self.kwargs["service_args"].extend(service_args)

            self.browser=getattr(self._driver, self._driver_name)(**self.kwargs)
        else:
            self.browser=getattr(self._driver, self._driver_name)(**self.kwargs)

        #load confs :: possible instance level
        self.load_confs(taskConfs)

        #waits
        self.browser.implicitly_wait(max_implicity)
        self.browser.set_page_load_timeout(max_timeout)

    def get_page_source(self):
        '''
        '''
        return self.browser.page_source

    def page_source(self, **kwargs):
        '''
        '''
        source=self.browser.page_source
        url=self.browser.current_url
        if 'target_url' in kwargs:
            url=kwargs['target_url']
        if "action_data" in kwargs:
            kwargs=kwargs["action_data"]
        return Helpers.save_page_source(url, source, **kwargs)

    def back(self, **kwargs):
        '''
        '''
        self.browser.back()

    def toMainPage(self, **kwargs):
        '''
        '''
        self.browser.switch_to_default_content()

    def get(self, url):
        '''
        '''
        self.browser.get(url)

    def close(self):
        '''
        '''
        if self.browser:
            if self._driver_name == 'PhantomJS':
                self.browser.service.process.send_signal(signal.SIGTERM)
            self.browser.quit()
        if self.proxy:
            self.proxy.close()
        return

    @property
    def current_url(self):
        '''
        '''
        return self.browser.current_url

    def execute_script(self, page_data, action_data):
        '''
        '''
        field_name=action_data['field_name']
        script=action_data['script']
        value=self.browser.execute_script(script)
        if isinstance(value, (list,dict)):
            value=json.dumps(value)
        page_data['page_data'].append(
                {field_name:[value,], 'index':-1})
        return

    def wait_3_seconds(self, **kwargs):
        '''
        '''
        time.sleep(3)

    def switch_to_frame(self, action_data, **kwargs):
        '''
        '''
        try:
            framis=self.browser.find_element_by_xpath(action_data["xpath"])
            if not framis:
                print("[-] Fail to find frame")
                return
            self.browser.switch_to_frame(framis)
        except Exception as e:
            print("[-] Fail to grab frame: {}".format(e))
            return

    def take_screenshot(self, action_data, **kwargs):
        """
        """
        url=self.browser.current_url
        screenshot=self.browser.get_screenshot_as_base64()
        Helpers.save_screenshot(url, screenshot, job=action_data["job"])

    def switch_to_secondWindow(self, action_data, **kwargs):
        """
        """
        try:
            #index=action_data["windown_index"]
            #for now a dumb switch -- only to the second window
            self.window_base=self.browser.window_handles[0]
            self.browser.switch_to_window(self.browser.window_handles[1])
        except Exception as e:
            print("[-] Fail to switch to  window: {}".format(e))
            return

    def toMainWindow(self):
        """
        """
        if not self.window_base: raise Exception("[-] No base window found")
        self.browser.close() #close currnent - second-window
        #move to base window
        self.browser.switch_to_window(self.window_base)

    def clickByJS(self, element, **kwargs):
        """
        """
        self.browser.execute_script("arguments[0].click()", element)

class BaseRequests:
    '''
    '''
    def __init__(self):
        '''
        '''
        self._headers=None
        self._cookies=None
        self.browser={}
        self.proxy=None

    def build_driver(self, proxy=None):
        '''
        '''
        if proxy:
            raise NotImplemented('[+] Proxy not available in lean requests ')
        session=requests.Session()
        session.headers=self._headers
        self.browser['session']=session

    def set_cookies(self, **cookies):
        '''
        '''
        raise NotImplemented('[-] Not implemeted yet::must be a CookieJar')

    def get_page_source(self):
        '''
        '''
        return self.browser['source']

    def page_source(self, **kwargs):
        '''
        '''
        source=self.browser['source']
        url=self.browser['url']
        if 'target_url' in kwargs:
            url=kwargs['target_url']
        Helpers.save_page_source(url, source, **kwargs)

    def back(self, **kwargs):
        '''
        '''
        raise TypeError('Requests driver does not have history')

    def get(self, url, allow_redirects=False):
        '''
        '''
        result=self.browser['session'].get(url, allow_redirects=allow_redirects)
        if result.status_code != 200:
            msg='LeanRequests GET fail. Headers [{}]'.format(result.headers)
            raise Exception(msg)
        self.browser['url']=url
        self.browser['source']=result.text
        self.browser['headers']=result.headers

    def close(self):
        '''
        '''
        if not self.browser.get('session'):return
        self.browser['session'].close()
        self.browser={}

    @property
    def current_url(self):
        '''
        '''
        return self.browser['url']

    def get_header_field(self, page_data, action_data):
        '''
        '''
        header_field=action_data['header_field']
        header_value=self.browser['headers'].get(header_field, 'None')
        page_data['page_data'].append(
                {header_field:[header_value,], 'index':-1})
        return

    def wait_3_seconds(self, **kwargs):
        '''
        '''
        time.sleep(3)



class DriverChoices:
    '''
    '''
    _choices=[]

    @classmethod
    def register(cls, driverClass):
        '''
        '''
        cls._choices.append(driverClass.__name__)

    @classmethod
    def get_all(cls):
        '''
        '''
        return cls._choices
