from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from drivers.drivers_base import BaseSeleniumBrowser, DriverChoices, BaseRequests



class SeleniumPhantom(BaseSeleniumBrowser):
    '''
    '''
    def __init__(self):
        '''
        '''
        super().__init__('PhantomJS')

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
        print('DRIVER SCRIPT=====', script)
        return self.browser.execute('executePhantomScript',
            {'script': script, 'args': args})


    def set_header(self, confObject):
        '''
        '''

        headers={h.field_name:h.field_value
            for h in confObject.driver.headers.all()
            #Accept-Encoding - avoid phantom bug
            if h.field_name not in ['Accept-Encoding']}

        print('========HEADERS', headers)

        header_scrit="""
        this.customHeaders = {headers};
        """.format(headers=str(headers))

        self.driver_script(header_scrit)

    def load_confs(self, confObject):
        '''
        '''
        #prepare phantomjs driver call
        self.phantom_command()
        #load headers
        self.set_header(confObject)
        #specific confs
        self.browser.set_window_size(1124, 850)
        self.pid=self.browser.service.process.pid

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

    def load_confs(self, confObject):
        '''
        '''
        headersObj=confObject.driver.headers.all()
        if headersObj.count():
            headers={h.field_name:h.field_value
                     for h in headersObj}
            self.set_header(**headers)

    def set_header(self, **kwargs):
        '''
        '''
        self._headers=kwargs


DriverChoices.register(SeleniumPhantom)
DriverChoices.register(LeanRequests)
DriverChoices.register(SeleniumRC)
