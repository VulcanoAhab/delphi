from django.contrib import admin
from drivers.models import Driver, Header, Cookie 
# Register your models here.


class DriverAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['name', 'type']



admin.site.register(Driver, DriverAdmin)
admin.site.register(Header)
admin.site.register(Cookie)
