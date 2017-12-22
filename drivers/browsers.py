from functools import partial
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from drivers.drivers_base import BaseSeleniumBrowser, DriverChoices, BaseRequests



class SeleniumPhantom(BaseSeleniumBrowser):
    '''
    '''
    def __init__(self):
        '''
        '''
        super().__init__('PhantomJS')
        self._headers={}
        self._header_name=''

    def phantom_command(self):
        '''
        '''
        script_for_status="""
        this.onResourceReceived = function(request) {
        this.request_response=request
        }.bind(this);
        """
        #add phantomjs execute endpoint
        phantom_exc_uri='/session/$sessionId/phantom/execute'
        cmds=self.browser.command_executor._commands
        cmds['executePhantomScript'] = ('POST', phantom_exc_uri)
        self.browser.execute('executePhantomScript',
            {'script': script_for_status, 'args': []})


    def driver_script(self, script, args=[]):
        '''
        run scripts with phantom internal
        '''
        return self.phantom_call({'script': script, 'args': args})


    def set_header(self, confObject):
        '''
        '''
        headersObj=[h for h in confObject.driver.headers.all()]
        if not len(headersObj):return
        self._headers={h.field_name:h.field_value
            for h in headersObj
            #Accept-Encoding - avoid phantom bug
            if h.field_name not in ['Accept-Encoding']}
        self._header_name=headersObj[0].header_name
        header_scrit="""
        this.customHeaders = {headers};
        """.format(headers=str(self._headers))

        self.driver_script(header_scrit)

    def load_confs(self, confObject):
        '''
        '''
        #prepare phantomjs driver call
        self.phantom_command()
        self.phantom_call=partial(self.browser.execute, 'executePhantomScript')

        #load headers
        self.set_header(confObject)
        #specific confs
        self.browser.set_window_size(1124, 850)
        self.pid=self.browser.service.process.pid

    def get_headers(self):
        '''
        ** Cookie from response + Request headers **
        '''
        cookie_script="""
        return this.cookies;
        """
        if 'Cookie' in self._headers:return self._headers
        cookies=self.driver_script(cookie_script)['value']
        cookie_string=' ;'.join(['{}={}'.format(c['name'],c['value'])
                                for c in cookies])
        self._headers.update({'Cookie':cookie_string})
        return self._headers

    def xpathToaction(self, xpathSelector):
        """
        """
        return self.browser.find_elements_by_xpath(xpathSelector)

class SeleniumRC(BaseSeleniumBrowser):
    '''
    '''
    def __init__(self):
        '''
        '''
        super().__init__('Remote')
        self._port=4444
        self._host='127.0.0.1'
        self._command_executor=None
        self._exec_str='http://{host}:{port}/wd/hub'
        self._remote_type=DesiredCapabilities.FIREFOX

    def load_confs(self, confObject):
        '''
        '''
        if confObject.driver.port:
            self._port=confObject.driver.port
        if confObject.driver.host:
            self._host=confObject.driver.host
        if confObject.driver.remote_browser_type:
            rbt=confObject.driver.remote_browser_type.upper()
            self._remote_type=getattr(DesiredCapabilities, rbt)
        self._command_executor=self._exec_str.format(host=self._host,
                                                     port=self._port)

    def build_driver(self, proxy_port=None):
        '''
        '''
        if proxy_port:
            raise NotImplemented('[-] Proxy not working \
            with remote server yet')
        if not self._command_executor:
            self._command_executor=self._exec_str.format(host=self._host,
                                                         port=self._port)
        self.browser=getattr(self._driver, self._driver_name)(
                                command_executor=self._command_executor,
                                desired_capabilities=self._remote_type)

class LeanRequests(BaseRequests):
    '''
    '''
    def __init__(self):
        '''
        '''
        super().__init__()
        self._headers={}
        self._header_name=''

    def load_confs(self, confObject):
        '''
        '''
        headersObj=[h for h in confObject.driver.headers.all()]
        if not len(headersObj):return
        headers={h.field_name:h.field_value
                     for h in headersObj}
        self.set_header(**headers)
        self._header_name=headersObj[0].header_name


    def set_header(self, **kwargs):
        '''
        '''
        self._headers=kwargs


class SeleniumChrome(BaseSeleniumBrowser):
    '''
    '''
    def __init__(self):
        '''
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        super().__init__('Chrome', chrome_options=options)
        self._headers={}
        self._header_name=''


    def set_header(self, confObject):
        '''
        '''
        headersObj=[h for h in confObject.driver.headers.all()]
        if not len(headersObj):return
        self._headers={h.field_name:h.field_value
            for h in headersObj
            #Accept-Encoding - avoid phantom bug
            if h.field_name not in ['Accept-Encoding']}
        self._header_name=headersObj[0].header_name
        header_scrit="""
        this.customHeaders = {headers};
        """.format(headers=str(self._headers))

        self.driver_script(header_scrit)

    def load_confs(self, confObject):
        '''
        '''
        #load headers
        self.set_header(confObject)
        #specific confs
        self.browser.set_window_size(1124, 850)
        self.pid=self.browser.service.process.pid


    def xpathToaction(self, xpathSelector):
        """
        """
        return self.browser.find_elements_by_xpath(xpathSelector)

DriverChoices.register(SeleniumPhantom)
DriverChoices.register(LeanRequests)
DriverChoices.register(SeleniumRC)
DriverChoices.register(SeleniumChrome)
