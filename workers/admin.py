from django.contrib import admin
from workers.models import Job, JobConfig, Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    '''
    '''
    list_display=('target_url', 'status')
    list_filter=('status',)

admin.site.register(Job)
admin.site.register(JobConfig)
admin.site.register(Task, TaskAdmin)
