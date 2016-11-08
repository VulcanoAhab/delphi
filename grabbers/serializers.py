from rest_framework import serializers
from grabbers.models import (Target,
                             Extractor,
                             ElementAction,
                             PageAction,
                             PostElementAction,
                             Grabber,
                             Mapper,
                             IndexedGrabber,
                             Sequence)


# == Serializers Models ==
class TargetSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Target
        fields=('field_name','field_selector', 'selector_type')

class ExtractorSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Extractor
        fields=('type',)


class ElementActionSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=ElementAction
        fields=('type','index')

class PageActionSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=PageAction
        fiels=('type','index')

class GrabberSerializer(serializers.ModelSerializer):
    target=TargetSerializer()
    extractors=ExtractorSerializer(many=True)
    element_action=ElementActionSerializer()
    page_action=PageActionSerializer()
    class Meta:
        model=Grabber
        fields=('name','extractors', 'element_action',
                'page_action', 'target', 'post_action',
                'created_at', 'last_modified')

class PostElementActionSerializer(serializers.ModelSerializer):
    grabber=GrabberSerializer()
    class Meta:
        model=PostElementAction
        fields=('name','grabber')

class MapperSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Mapper
        fields=('name','field_name', 'field_selector', )


class IndexedGrabberSerializer(serializers.ModelSerializer):
    '''
    '''
    grabber=GrabberSerializer()
    class Meta:
        model=IndexedGrabber
        fields=('grabber', 'sequence_index')

class SequenceSerializer(serializers.ModelSerializer):
    '''
    '''
    indexed_grabbers=IndexedGrabberSerializer(many=True)
    class Meta:
        model=Sequence
        fields=('indexed_grabbers', 'name')
