from django.db import models
import hashlib
import datetime
import urllib.parse as uparse

# Create your models here.

### --- helpers ---- deprecated --
def site_directory_path(instance, filename):
    job_name=instance.job.name
    return '{job_name}/htmls/{uid}.html'.format(
                        job_name=job_name,
                        uid=instance.addr.url_id)


def make_url_id(url_string):
    '''
    '''
    umd5=hashlib.md5()
    umd5.update(url_string.encode())
    return umd5.hexdigest()

#### --- models ------
class Locator(models.Model):
    '''
    '''

    url=models.URLField(max_length=2000)
    url_id=models.CharField(max_length=150, unique=True)
    uround=models.IntegerField(default=-1)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    class Meta:
        '''
        '''
        verbose_name='Url'
        verbose_name_plural='Urls'


    def __str__(self):
        '''
        '''
        return self.url[:150]


    def save(self, *args, **kwargs):
        '''
        '''
        if not self.url_id:
            self.url_id=make_url_id(self.url)
        super().save(*args, **kwargs)


class Page(models.Model):
    '''
    '''
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    html=models.TextField()
    addr=models.ForeignKey('urlocators.Locator')
    job=models.ForeignKey('workers.Job')

    def __str__(self):
        '''
        '''
        return self.addr.url
