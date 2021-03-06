from django.db import models
from drivers.browsers import DriverChoices
# Create your models here.

class Header(models.Model):
    '''
    '''
    field_name=models.CharField(max_length=150)
    field_value=models.TextField()
    header_name=models.CharField(max_length=150)

    def __str__(self):
        '''
        '''
        return '{name}[{field}]'.format(
                                name=self.header_name,
                                field=self.field_name
                                        )


class Driver(models.Model):
    '''
    '''
    _doices=[(dc,dc) for dc in DriverChoices.get_all()]
    name=models.CharField(max_length=250, unique=True)
    type=models.CharField(max_length=50, choices=_doices)
    headers=models.ManyToManyField('drivers.Header', blank=True)
    host=models.CharField(max_length=250, blank=True, null=True)
    port=models.IntegerField(blank=True, null=True)
    remote_browser_type=models.CharField(max_length=250, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    # cookies=models.ManyToManyField('drivers.Cookie', blank=True)

    def __str__(self):
        '''
        '''
        return self.name
