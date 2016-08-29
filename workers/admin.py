from django.contrib import admin
from workers.models import Job, TaskConfig, Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=('target_url', 'status')
    list_filter=('status', 'job__name')


class TaskInline(admin.StackedInline):
    '''
    '''
    model=Task

class JobAdmin(admin.ModelAdmin):
    '''
    '''
    inlines=[TaskInline,]

admin.site.register(Job)
admin.site.register(TaskConfig)
admin.site.register(Task, TaskAdmin)
