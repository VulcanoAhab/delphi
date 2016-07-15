from django.contrib import admin
from drivers.models import Driver, Header, Cookie 
# Register your models here.


class DriverAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['name', 'type']

<<<<<<< HEAD
class HeaderAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['header_name', 'field_name', 'field_value']


admin.site.register(Driver, DriverAdmin)
admin.site.register(Header, HeaderAdmin)
admin.site.register(Cookie)
