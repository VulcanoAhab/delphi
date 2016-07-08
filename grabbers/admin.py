from django.contrib import admin
from grabbers.models import Grabber, Target, Extractor, ElementAction, Sequence, PostElementAction, Mapper, PageAction, IndexedGrabber


class SequenceAdmin(admin.ModelAdmin):
    '''
    '''
    filter_horizontal=['indexed_grabbers',]

admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Mapper)
admin.site.register(IndexedGrabber)
admin.site.register(Grabber)
admin.site.register(Target)
admin.site.register(Extractor)
admin.site.register(PostElementAction)
admin.site.register(ElementAction)
admin.site.register(PageAction)
