from django.db import models


_SPATTERN = [
        #('cs', 'css'),
        ('xp', 'xpath'),
    ]

class Action(models.Model):
    '''
    '''
    _dos=[
        ('click','click')
    ]
    name=models.CharField(max_length=150)
    type=models.CharField(max_length=10, choices=_dos, default='click')
    index=models.IntegerField(default=0)
    
    def __str__(self):
        '''
        '''
        return self.name

class PostActTarget(models.Model):
    '''
    '''
    
    field_name=models.CharField(max_length=250)
    field_selector=models.CharField(max_length=250)
    selector_type=models.CharField(max_length=2, choices=_SPATTERN, default='xp')
    extractors=models.ManyToManyField('grabbers.Extractor', blank=True)
    actions=models.ManyToManyField('grabbers.Action', related_name='actions',  blank=True)
    act=models.ForeignKey('grabbers.Action', related_name='act')
    
    def __str__(self):
        '''
        '''
        return self.field_name


class Extractor(models.Model):
    '''
    '''
    attr=models.CharField(max_length=50)
    
    def __str__(self):
        '''
        '''
        return self.attr

class Target(models.Model):
    '''
    '''
    field_name=models.CharField(max_length=250)
    field_selector=models.CharField(max_length=250)
    selector_type=models.CharField(max_length=2, choices=_SPATTERN, default='xp')
    extractors=models.ManyToManyField('grabbers.Extractor', blank=True)
    actions=models.ManyToManyField('grabbers.Action', blank=True)
    grabber=models.ForeignKey('grabbers.Grabber')
    

    def __str__(self):
        '''
        '''
        return self.field_name

class Grabber(models.Model):
    '''
    '''
    name=models.CharField(max_length=250, unique=True)
    sequence_index=models.IntegerField(default=0)

    def __str__(self):
        '''
        '''
        return self.name


class Sequence(models.Model):
    '''
    '''
    grabbers=models.ManyToManyField('grabbers.Grabber')
    name=models.CharField(max_length=150)

    def __str__(self):
        '''
        '''
        return self.name



