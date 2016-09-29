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
from django.db

#db models
from urlocators.models import Page, Locator, make_url_id

#===========================================================#
#=================== Drivers helpers =======================#
class Helpers:
    '''
    '''
    @staticmethod
    def save_page_source(url, source, **kwargs):
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
        except:
            db.close_old_connections()
            locs=Locator.objects.get(url_id=url_id)
        except ObjectDoesNotExist:
            locs=Locator()
            locs.url=url
            locs.save()
        try:
            page=Page.objects.get(addr=locs.id, job=job)
        except ObjectDoesNotExist:
            page=Page()
            #build html file
            page.job=job
            page.addr=locs
            fp=tempfile.TemporaryFile()
            fp.write(source.encode())
            fp.seek(0)
            file_html=File(fp)
            page.html=file_html
            page.save()
            fp.close()
            #close temp file
        print('[+] Done saving page [{}]'.format(url[:150]))
        if ('return_page' in kwargs
            and kwargs['return_page']):
            return page

#===========================================================#
#==================== Drivers base classes =================#
class BaseSeleniumBrowser:
    '''
    '''
    def __init__(self, driver_name, remote_server):
        '''
        '''
        self._driver_name=driver_name
        self._driver=webdriver
        self.remote_server=remote_server
        self.host=''
        self.pid=None
        self.browser=None
        self.proxy=None

    def set_host(self, host):
        '''
        '''
        self.host=host

    def build_driver(self, proxy_port=None):
        '''
        '''
        #set browser global waits
        max_implicity=5
        max_timeout=30
        if proxy_port:
            proxy_addr='--proxy=127.0.0.1:{}'.format(proxy_port)
            service_args=[proxy_addr, '--ignore-ssl-errors=yes']
            self.browser=getattr(self._driver, self._driver_name)(service_args=service_args)
        else:
            self.browser=getattr(self._driver, self._driver_name)()
        #phantom window spec
        if self._driver_name == 'PhantomJS':
            self.browser.set_window_size(1124, 850)
            self.pid=self.browser.service.process.pid
        #waits
        self.browser.implicitly_wait(max_implicity)
        self.browser.set_page_load_timeout(max_timeout)

    def set_cookies(self, **cookies):
        '''
        '''
        if not self.host:
            raise Exception('Host is required for cookie seting')
        self.browser.get(self.host)
        for key,value in cookies.items():
            self.browser.add_cookie({'name':key, 'value':value})

    def get_page_source(self):
        '''
        '''
        return self.browser.page_source

    def page_source(self, **kwargs):
        '''
        '''
        source=self.browser.page_source
        url=self.browser.current_url
        return Helpers.save_page_source(url, source, **kwargs)

    def back(self, job,  **kwargs):
        '''
        '''
        self.browser.back()

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

    def switch_to_frame(self, **kwargs):
        '''
        '''
        raise NotImplemented('Not implemented yet')


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
