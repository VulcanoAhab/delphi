
import os

from django.db import models
from django.conf import settings

# Create your models here.

class Proxy(models.Model):
    '''
    '''
    _status=[
        ('on', 'on'),
        ('off', 'off'),
            ]
    _proxs=[
        ('browsermobproxy', 'browsermobproxy')
            ]


    _mobCallPath=os.path.join(settings.BASE_DIR,
                              'proxy',
                              'utils',
                              'browsermob-proxy',
                              'bin',
                              'browsermob-proxy')

    type=models.CharField(max_length=50, choices=_proxs, default='browsermobproxy', unique=True)
    call=models.CharField(max_length=150, default=_mobCallPath)
    status=models.CharField(max_length=3, default='off', choices=_status)

    class Meta:
        verbose_name_plural='Proxies'

    def __str__(self):
        '''
        '''
        return self.type


class Entry(models.Model):
    '''
    '''
    url=models.URLField(max_length=500)
    method=models.CharField(max_length=50)
    dest_ip=models.GenericIPAddressField()
    job_id=models.IntegerField()
    duration=models.IntegerField()
    content_type=models.CharField(max_length=150)
    target_url=models.URLField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return '::'.join([str(self.job_id), self.url[:75]])

