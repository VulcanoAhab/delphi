from django.contrib import admin

from proxy.models import Proxy, Entry
import urllib.parse as uparse

class AdminEntry(admin.ModelAdmin):
    '''
    '''
    list_display=['netloc', 'path', 'dest_ip', 'response_status', 'duration', 'target_url']
    search_fields=['url', 'dest_ip']
    list_filter=['response_status',]

    def netloc(self, obj):
        '''
        '''
        url=uparse.urlparse(obj.url)
        return url.netloc

    def path(self, obj):
        '''
        '''
        url=uparse.urlparse(obj.url)
        return url.path

admin.site.register(Proxy)
admin.site.register(Entry, AdminEntry)

