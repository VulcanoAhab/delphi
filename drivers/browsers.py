from drivers.drivers_base import BaseSeleniumBrowser, DriverChoices



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

class PlainRequests:
    '''
    '''
    def __init__(self, remote_server=False):
        '''
        '''
        raise NotImplemented('Not developed yet')

DriverChoices.register(SeleniumPhantom)
