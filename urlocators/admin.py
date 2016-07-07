from django.contrib import admin
from urlocators.models import Locator, Page

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=('page_url', 'job_names')
    readonly_fields=('created_at', 'modified_at')
    search_fields=('locator__url','job__seed')

    def page_url(self, obj):
        '''
        '''
        if obj.addr:
            return obj.addr.url[:150]
        return 'nourl'

    def job_names(self, obj):
        '''
        '''
        if obj.job:
            return obj.job.name
        return 'nojob'

class LocatorAdmin(admin.ModelAdmin):
    '''
    '''
    readonly_fields=['url_id','created_at']

admin.site.register(Page, PageAdmin)
admin.site.register(Locator, LocatorAdmin)
