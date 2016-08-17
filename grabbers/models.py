from django.db import models


_SPATTERN = [
        #('cs', 'css'),
        ('xpath', 'xpath'),
        ('regex', 'regex'),
    ]


class PageAction(models.Model):
    '''
    '''
    _pa=[
        ('back','back'),
        ('page_source', 'page_source'),
        ('get_header_field', 'get_header_field'),
        ('switch_to_frame', 'switch_to_frame'),
    ]
    type=models.CharField(max_length=50, choices=_pa, default='page_source')
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
    type=models.CharField(max_length=50, choices=_dos, default='click')
    index=models.IntegerField(default=0)

    def __str__(self):
        '''
        '''
        return '::'.join([self.type, str(self.index)])

class PostElementAction(models.Model):
    '''
    '''
    name=models.CharField(max_length=250)
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
            ]

    type=models.CharField(max_length=100, choices=_exChoices)

    def __str__(self):
        '''
        '''
        return self.type

class Target(models.Model):
    '''
    '''
    field_name=models.CharField(max_length=250)
    field_selector=models.CharField(max_length=250)
    selector_type=models.CharField(max_length=10, choices=_SPATTERN, default='xpath')

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
    page_action=models.ForeignKey('grabbers.PageAction', blank=True, null=True)

    def __str__(self):
        '''
        '''
        return self.name


class Grabber(models.Model):
    '''
    '''
    name=models.CharField(max_length=250, unique=True)
    extractors=models.ManyToManyField('grabbers.Extractor', blank=True)
    element_action=models.ForeignKey('grabbers.ElementAction', blank=True, null=True)
    page_action=models.ForeignKey('grabbers.PageAction', blank=True, null=True)
    target=models.ForeignKey('grabbers.Target', blank=True, null=True)
    post_action=models.ForeignKey('grabbers.PostElementAction', related_name='post_element_grabber', blank=True, null=True)

    def __str__(self):
        '''
        '''
        return self.name


class IndexedGrabber(models.Model):
    '''
    '''
    grabber=models.ForeignKey('grabbers.Grabber')
    sequence_index=models.IntegerField(default=0)

    def __str__(self):
        '''
        '''
        return '::'.join([self.grabber.name, str(self.sequence_index)])

class Sequence(models.Model):
    '''
    '''
    indexed_grabbers=models.ManyToManyField('grabbers.IndexedGrabber')
    name=models.CharField(max_length=150)

    def __str__(self):
        '''
        '''
        return self.name



