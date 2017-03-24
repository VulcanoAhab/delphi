
class PhantomScripts:
    '''
     *** it will be integrated to the browser ***
    '''

    _caller=None

    _text="""
        return this.plainText
        """

    _response_status="""
        return this.request_response
    """

    _server_banner="""
        return this.request_response
    """

    @classmethod
    def load_browser(cls, browser):
        '''
        '''
        cls._caller=browser.driver_script

    @classmethod
    def text(cls):
        '''
        '''
        return cls._caller(cls._text)

    @classmethod
    def response_status(cls):
        '''
        '''
        return cls._caller(cls._response_status)[['value'][0]['status']

    @classmethod
    def server_banner(cls):
        '''
        '''
        headers=cls._caller(cls._server_banner)['value'][0]['headers']
        for header in headers:
            if header.get('name','').lower() != 'server':continue
            return header.get('value','').lower()
        return ''


class Condis:
    '''
    '''
    type=None
    relation=None
    value=None

    _rels={
        'equal':lambda x,y:x==y,
        'different':lambda x,y:x!=y,
        'contains':lambda x,y: x.lower() in y.lower()
        'do_not_contain':lambda x,y: x.lower() not in y.lower()
    }

    @classmethod
    def _text(cls, page_text):
        '''
        '''
        fn=cls._rels[cls.relation]
        return fn(cls.value.strip().lower(), page_text.lower())


    @classmethod
    def test(cls, browser):
        '''
        '''
        _t={
            'text':cls._text,
            'response_status':cls._status,
            'server_banner':cls._banner,
            'status_and_banner':cls._status_and_banner,
        }
        #test for browser -- methods only tested with selenium driver (yet)
        browser_name=browser.__class__.__name__
        if browser_name != 'SeleniumPhantom':
            raise TypeError('[-] Only SeleniumPhantom has conditions yet')
        #perform test
        PhantomScripts.load_browser(browser)
        base_value=getattr(PhantomScripts, cls.type)()
        return _t[cls.type](base_value)
