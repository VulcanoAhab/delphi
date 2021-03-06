from django.contrib import admin
from grabbers.models import *
from workers.models import TaskConfig

class SequenceAdmin(admin.ModelAdmin):
    '''
    '''
    filter_horizontal=['indexed_grabbers',]


class TargetAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields=['field_name',]

class ConditionAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields=['value',]
    list_filter=['type','relation']


class GrabbersAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields=['name',]

class InlineTaskConfig(admin.StackedInline):
    '''
    '''
    model=TaskConfig


class MapperAdmin(admin.ModelAdmin):
    '''
    '''
    inlines=[InlineTaskConfig,]

admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Mapper, MapperAdmin)
admin.site.register(IndexedGrabber)
admin.site.register(Grabber, GrabbersAdmin)
admin.site.register(Target,TargetAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Extractor)
admin.site.register(PostElementAction)
admin.site.register(ElementAction)
admin.site.register(PageAction)
