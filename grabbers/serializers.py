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
    field_name=serializers.CharField(max_length=250)

    class Meta:
        model=Target
        fields=('field_name', 'field_selector', 'selector_type')
        #extra_kwargs = {'field_name': {'unique': False}}

    def save(self):
        '''
        '''
        field_name=self.validated_data['field_name']
        target,created=Target.objects.get_or_create(field_name=field_name)
        if created:
            for k,v in self.validated_data.items():
                if k == 'field_name':continue
                setattr(target,k,v)
            target.save()



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
    element_action=ElementActionSerializer(allow_null=True, required=False)
    page_action=PageActionSerializer(allow_null=True, required=False)
    name=serializers.CharField(max_length=250)

    class Meta:
        model=Grabber
        fields=('name','extractors', 'element_action',
                'page_action', 'target', 'post_action',
                'created_at', 'last_modified')

    def save(self):
        '''
        '''
        name=self.validated_data['name']
        target,created=Target.objects.get_or_create(name=name)
        if created:
            for k,v in self.validated_data.items():
                if k == 'name':continue
                setattr(target,k,v)
            target.save()

    def create(self):
        '''
        '''
        extractors=self.validated_data.pop('extractors')
        extractorsObj=Extractor.get_or_create(type=extractors['type'])


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
