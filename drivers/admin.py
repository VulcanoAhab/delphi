from django.contrib import admin
from drivers.models import Driver, Header
# Register your models here.


class DriverAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['name', 'type']

class HeaderAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['header_name', 'field_name', 'field_value']
    list_filter=['header_name', 'field_name']
    search_fields=['field_name','field_value','header_name']


admin.site.register(Driver, DriverAdmin)
admin.site.register(Header, HeaderAdmin)
# admin.site.register(Cookie)
