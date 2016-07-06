from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#django
from django.core.files import File

#db models
from urlocators.models import Page, Locator, make_url_id

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

    def set_host(self, host):
        '''
        '''
        self.host=host

    def build_driver(self, **kwargs):
        '''
        '''
        if kwargs:
            self.browser=getattr(self._driver, self._driver_name)(**kwargs)
        else:
            self.browser=getattr(self._driver, self._driver_name)()
        if self._driver_name == 'PhantomJS':
            self.browser.set_window_size(1124, 850)

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

    def page_source(self, job):
        '''
        '''
        source=self.browser.page_source
        url=self.browser.current_url
        url_id=make_url_id(url)

        #build url relations
        locs, created=Locator.objects.get_or_create(url_id=page_url_id)
        if created:
            locs.url=page_url
            locs.save()

        #build page relations
        page,created=Page.objects.get_or_create(url=locs)
        if created:
            #build html file
            fp=tempfile.TemporaryFile()
            fp.write(page_source.encode())
            fp.seek(0)
            file_html=File(fp)
            page.html=file_html
            page.job.add(cls._job)
            page.url=locs
            page.save()
            #close temp file
            fp.close()
        print('[+] Done saving page')

    def back(self):
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
        if not self.browser:return
        self.browser.close()

    @property
    def current_url(self):
        '''
        '''
        return self.browser.current_url

    def wait_for_element(self, target_element, eltype, timeout=30):
        '''
        wait for html element to load
        for now, only working with xpath pattern
        '''
        timeout=timeout
        eltypeDict={'xpath':By.XPATH,}
        target=(eltypeDict[eltype], target_element)
        try:
            element_present = EC.presence_of_element_located(target)
            WebDriverWait(self.browser, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")


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
