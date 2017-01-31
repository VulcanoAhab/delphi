from base import Model

class Extractor(Model):
    '''
    '''
    fields=['type',]

    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj=obj)

class Target(Model):
    '''
    '''
    fields=['field_name', 'field_selector','selector_type',
            'created_at', 'last_modified']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj=obj)


class ElementAction(Model):
    '''
    '''
    fields=['type', 'index']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj={})

class PageAction(Model):
    '''
    '''
    fields=['type', 'index']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj={})

class Mapper(Model):
    '''
    '''
    fields=['name','field_name','field_selector', 'created_at','last_modified']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj={})

class Grabber(Model):
    '''
    '''
    fields=['name', 'extrator', 'element_action', 'page_action',
            'target', 'post_action', 'created_at', 'last_modified']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj={})

class IndexedGrabber(Model):
    '''
    '''
    fields=['grabber', 'sequence_index', 'created_at', 'last_modified']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj={})

class Sequence(Model):
    '''
    '''
    fields=['indexed_grabbers', 'name', 'created_at', 'last_modified']
    def __init__(self, **kwargs, obj={}):
        '''
        '''
        super().__init__(**kwargs, obj={})
