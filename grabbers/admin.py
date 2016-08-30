from django.contrib import admin
from grabbers.models import Grabber, Target, Extractor, ElementAction, Sequence, PostElementAction, Mapper, PageAction, IndexedGrabber


class SequenceAdmin(admin.ModelAdmin):
    '''
    '''
    filter_horizontal=['indexed_grabbers',]


class TargetAdmin(admin.ModelAdmin):
    '''
    '''
    search_fields=['field_name',]

admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Mapper)
admin.site.register(IndexedGrabber)
admin.site.register(Grabber)
admin.site.register(Target,TargetAdmin)
admin.site.register(Extractor)
admin.site.register(PostElementAction)
admin.site.register(ElementAction)
admin.site.register(PageAction)
