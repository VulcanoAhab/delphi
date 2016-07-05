from django.contrib import admin
from urlocators.models import Locator, Page

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=('page_url', 'job_names')
    readonly_fields=('created_at', 'modified_at')
    search_fields=('url__url','job__seed__url')

    def page_url(self, obj):
        '''
        '''
        return obj.url.url[:150]
    
    def job_names(self, obj):
        '''
        '''
        return ','.join([j.name for j in obj.job.all()])

class LocatorAdmin(admin.ModelAdmin):
    '''
    '''
    readonly_fields=['url_id','created_at']

admin.site.register(Page, PageAdmin)
admin.site.register(Locator, LocatorAdmin)
