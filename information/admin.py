from django.contrib import admin
from information.models import PageData

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['field_name', 'page_url', 'data']

    def page_url(self, obj):
        '''
        '''
        return obj.page.url.url

    def data(self, obj):
        '''
        '''
        return ' '.join([obj.field_value[:150], '...'])


admin.site.register(PageData, PageAdmin)
