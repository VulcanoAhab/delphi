from api.utils.client.base import Model

class Extractor(Model):
    '''
    '''
    fields=['type',]

    def __init__(self,  obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)

class Target(Model):
    '''
    '''
    fields=['field_name', 'field_selector','selector_type',
            'created_at', 'last_modified']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)


class ElementAction(Model):
    '''
    '''
    fields=['type', 'index']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)

class PageAction(Model):
    '''
    '''
    fields=['type', 'index']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)

class Mapper(Model):
    '''
    '''
    fields=['name','field_name','field_selector', 'created_at','last_modified']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)

class Grabber(Model):
    '''
    '''
    fields=['name', 'extrator', 'element_action', 'page_action',
            'target', 'post_action', 'created_at', 'last_modified']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)

class IndexedGrabber(Model):
    '''
    '''
    fields=['grabber', 'sequence_index', 'created_at', 'last_modified']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)

class Sequence(Model):
    '''
    '''
    fields=['indexed_grabbers', 'name', 'created_at', 'last_modified']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)


class Driver(Model):
    '''
    '''
    fields=['name', 'type', 'headers']
    def __init__(self, obj={}, **kwargs):
        '''
        '''
        super().__init__(obj={}, **kwargs)
