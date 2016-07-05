from django.db import models
import hashlib
import datetime
import urllib.parse as uparse

# Create your models here.

### --- helpers ----
def site_directory_path(instance, filename):
    job_name=instance.job.name
    return '{job_name}/htmls/{uid}.html'.format(
                        job_name=job_name,
                        uid=instance.url.url_id)


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
    
    url=models.URLField(max_length=1000)
    url_id=models.CharField(max_length=150, unique=True, blank=True)
    uround=models.IntegerField(default=-1)
    parent=models.ManyToManyField('self', related_name='parent', blank=True)
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
    url=models.ForeignKey('Locator', related_name='page_url')
    job=models.ManyToManyField('workers.Job')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    html=models.FileField(upload_to=site_directory_path)

    def __str__(self):
        '''
        '''
        return '-'.join([self.url.url[:150], ','.join([j.name for j in self.job.all()])])
