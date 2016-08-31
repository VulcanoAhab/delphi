from django.contrib import admin
from information.models import PageData

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=['field_name', 'page_url', 'data', 'element_index']
    list_filter=['field_name','page__job']
    search_fields=['page__addr__url', 'field_value']
    readonly_fields=['page', 'field_name', 'field_value', 'control_key', 'element_index']

    sort=['element_index']

    def page_url(self, obj):
        '''
        '''
        return obj.page.addr.url

    def data(self, obj):
        '''
        '''
        return ' '.join([obj.field_value[:150], '...'])


admin.site.register(PageData, PageAdmin)
