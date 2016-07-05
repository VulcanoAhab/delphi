from django.contrib import admin
from grabbers.models import Grabber, Target, Extractor, Action, Sequence, PostActTarget

class InlineTarget(admin.StackedInline):
    model=Target
    filter_horizontal=['extractors','actions' ]


class InlinePostAct(admin.StackedInline):
    model=PostActTarget
    filter_horizontal=['extractors','actions' ]

class ActionAdmin(admin.ModelAdmin):
    inlines=[InlinePostAct,]

class GrabberAdmin(admin.ModelAdmin):
    '''
    '''
    inlines=[InlineTarget,]

class PostActAdmin(admin.ModelAdmin):
    filter_horizontal=['extractors','actions' ]
   
class TargetAdmin(admin.ModelAdmin):
    filter_horizontal=['extractors','actions' ]

class SequenceAdmin(admin.ModelAdmin):
    '''
    '''
    filter_horizontal=['grabbers',]


admin.site.register(Grabber, GrabberAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Extractor)
admin.site.register(PostActTarget, PostActAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Sequence, SequenceAdmin)
