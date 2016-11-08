from django.db import models
from drivers.browsers import DriverChoices
# Create your models here.

class Header(models.Model):
    '''
    '''
    field_name=models.CharField(max_length=50)
    field_value=models.CharField(max_length=500)
    header_name=models.CharField(max_length=150)

    def __str__(self):
        '''
        '''
        return '{name}[{field}]'.format(
                                name=self.header_name,
                                field=self.field_name
                                        )

# class Cookie(models.Model):
#     '''
#     '''
#     field_name=models.CharField(max_length=50)
#     field_value=models.CharField(max_length=500)
#     cookie_name=models.CharField(max_length=50)
#
#     def __str__(self):
#         '''
#         '''
#         return self.cookie_name


class Driver(models.Model):
    '''
    '''
    _doices=[(dc,dc) for dc in DriverChoices.get_all()]
    name=models.CharField(max_length=250)
    type=models.CharField(max_length=50, choices=_doices)
    headers=models.ManyToManyField('drivers.Header', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    # cookies=models.ManyToManyField('drivers.Cookie', blank=True)

    def __str__(self):
        '''
        '''
        return self.name
