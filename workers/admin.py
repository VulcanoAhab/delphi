from django.contrib import admin
from workers.models import Job, JobConfig, Task
# Register your models here.

admin.site.register(Job)
admin.site.register(JobConfig)
admin.site.register(Task)
