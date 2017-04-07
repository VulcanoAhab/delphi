from lxml import html, etree

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
    def load_page(job, browser):
        '''
        '''
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