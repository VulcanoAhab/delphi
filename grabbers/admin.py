from django.contrib import admin
from grabbers.models import Grabber, Target, Extractor, ElementAction, Sequence, PostElementAction, Mapper, PageAction


admin.site.register(Sequence)
admin.site.register(Mapper)
admin.site.register(Grabber)
admin.site.register(Target)
admin.site.register(Extractor)
admin.site.register(PostElementAction)
admin.site.register(ElementAction)
admin.site.register(PageAction)
