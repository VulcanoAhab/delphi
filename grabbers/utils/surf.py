
class Paging:
    '''
    '''
    _find_type=''
    _find_value=''

    _bynu=''
    _expnu=''

    @classmethod
    def set_byNumbers(cls, xpath=None, expected_size=0):
        '''
        '''
        if xpath:
            cls._bynu=xpath
            cls._expnu=expected_size
            return
        expected_size=3
        rangis=range(2, 2+expected_size)
        frame='.//a[{}]'
        targets=' or '.join(["text()={}".format(tn)
                                for tn in rangis])
        cls._bynu=frame.format(targets)
        cls._expnu=expected_size
    
    @classmethod
    def find_byMumbers(cls, browser):
        '''
        '''
        pass

    

    @classmethod
    def find_byXpath(cls, browser):
        '''
        '''
        pass

    @classmethod
    def iter_toTarget(cls, browser, target_page):
        '''
        '''
        pass


