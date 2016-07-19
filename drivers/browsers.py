from drivers.drivers_base import BaseSeleniumBrowser, DriverChoices, BaseRequests



class SeleniumPhantom(BaseSeleniumBrowser):
    '''
    '''
    def __init__(self, remote_server=False):
        '''
        '''
        super().__init__('PhantomJS', remote_server=remote_server)

    def set_header(self, **kwargs):
        '''
        '''
        base='phantomjs.page.customHeaders.'
        for k,v in kwargs.items():
            k=''.join([base, k])
            self._driver.DesiredCapabilities.PHANTOMJS[k]=v

    def load_confs(self, confObject):
        '''
        '''
        headers={h.field_name:h.field_value
                 for h in confObject.driver.headers.all()}
        self.set_header(**headers)

class SeleniumFirefoxRC(BaseSeleniumBrowser):
    '''
    '''
    def __init__(self, remote_server=False):
        '''
        '''
        raise NotImplemented('Not developed yet')

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
