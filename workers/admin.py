from django.contrib import admin
from workers.models import Job, TaskConfig, Task, TaskProducer
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=('target_url', 'status')
    list_filter=('status', 'job__name')
    search_fields=['name', 'target_url']

class TaskConfigAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields=['name']


class TaskInline(admin.StackedInline):
    '''
    '''
    model=Task

class JobAdmin(admin.ModelAdmin):
    '''
    '''
    inlines=[TaskInline,]
    search_fields=['name']

admin.site.register(Job)
admin.site.register(TaskConfig, TaskConfigAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskProducer)
