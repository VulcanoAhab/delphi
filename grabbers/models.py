from django.db import models


_SPATTERN = [
        #('cs', 'css'),
        #('regex', 'regex'),
        ('xpath', 'xpath'),
        ('script', 'script'),
    ]

class Condition(models.Model):
    '''
    '''
    #commented items will be implemented
    _co=(
        'text', 'text',
        #'regex', 'regex'
        #'element', 'element',
        'response_status', 'response_status',
        'server_banner', 'server_banner',
        #'grabber_name', 'grabber_name'
    )
    _re=(
        'equal', 'equal',
        'different', 'different',
        'contain', 'contain',
        'do_not_contain','do_not_contain'
    )
    _st=(
        'silent','silent',
        'header', 'header',
        #'page_data','page_data'
    )
    type=models.CharField(max_length=50, choices=_co, default='text')
    relation=models.ChaField(max_length=50, choices=_re, default='equal')
    save_type=models.ChaField(max_length=50, choices=_st, default='silent')
    value=models.TextField()
    sequence=models.ForeignKey('grabbers.Sequence')


    def __str__(self):
        '''
        '''
        return '::'.join([self.type, self.relation, self.value[:50]])


class PageAction(models.Model):
    '''
    '''
    _pa=[
        ('back','back'),
        ('execute_script', 'execute_script'),
        ('get_header_field', 'get_header_field'),
        ('wait_3_seconds', 'wait_3_seconds'),
        ('save_headers', 'save_headers'),
        #('switch_to_frame', 'switch_to_frame'),
        #('scroll_page', 'scroll_page'),
            ]
    type=models.CharField(max_length=50, choices=_pa, default='page_source', unique=True)
    index=models.IntegerField(default=0)

    def __str__(self):
        '''
        '''
        return '::'.join([self.type, str(self.index)])



class ElementAction(models.Model):
    '''
    '''
    _dos=[
        ('click','click'),
    ]
    type=models.CharField(max_length=50, choices=_dos, default='click', unique=True)
    index=models.IntegerField(default=0) #legacy

    def __str__(self):
        '''
        '''
        return '::'.join([self.type, str(self.index)])

class PostElementAction(models.Model):
    '''
    '''
    name=models.CharField(max_length=250, unique=True)
    grabber=models.ForeignKey('grabbers.Grabber', related_name='grabber')

    def __str__(self):
        '''
        '''
        return self.name


class Extractor(models.Model):
    '''
    '''
    _exChoices=[
        ('href', 'href'),
        ('text_content', 'text_content'),
        ('generic_link', 'generic_link'),
        ('class', 'class'),
        ('id', 'id'),
        ('size', 'size'),
        ('title','title'),
        ('Location','Location'),
        ('style', 'style'),
        ('content', 'content')
            ]

    type=models.CharField(max_length=100, choices=_exChoices, unique=True)

    def __str__(self):
        '''
        '''
        return self.type

class Target(models.Model):
    '''
    '''
    field_name=models.CharField(max_length=250, unique=True)
    field_selector=models.TextField()
    selector_type=models.CharField(max_length=10, choices=_SPATTERN, default='xpath')
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return self.field_name


class Mapper(models.Model):
    '''
    '''
    name=models.CharField(max_length=250, unique=True)
    field_name=models.CharField(max_length=250)
    field_selector=models.CharField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return self.name


class Grabber(models.Model):
    '''
    '''
    name=models.CharField(max_length=250, unique=True)
    extractor=models.ForeignKey('grabbers.Extractor', blank=True, null=True)
    element_action=models.ForeignKey('grabbers.ElementAction', blank=True, null=True)
    page_action=models.ForeignKey('grabbers.PageAction', blank=True, null=True)
    target=models.ForeignKey('grabbers.Target', blank=True, null=True)
    post_action=models.ForeignKey('grabbers.PostElementAction', related_name='post_element_grabber', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return self.name


class IndexedGrabber(models.Model):
    '''
    '''
    grabber=models.ForeignKey('grabbers.Grabber')
    sequence_index=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return '::'.join([self.grabber.name, str(self.sequence_index)])

class Sequence(models.Model):
    '''
    '''
    indexed_grabbers=models.ManyToManyField('grabbers.IndexedGrabber')
    name=models.CharField(max_length=150, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return self.name
