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
from rest_framework.renderers import JSONRenderer

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
    target=TargetSerializer(read_only=True)
    extractors=ExtractorSerializer(many=True, read_only=True)
    element_action=ElementActionSerializer(read_only=True)
    page_action=PageActionSerializer(read_only=True)
    class Meta:
        model=Grabber
        fields=('name','extractors', 'element_action',
                'page_action', 'target', 'post_action',
                'created_at', 'last_modified')

class PostElementActionSerializer(serializers.ModelSerializer):
    grabber=GrabberSerializer(read_only=True)
    class Meta:
        model=PostElementAction
        fields=('name','grabber')

class MapperSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Mapper
        fields=('name','field_name', 'field_selector', )


class IndexedGrabberSerializer(serializer.ModelSerializer):
    '''
    '''
    pass

class SequenceSerializer(serializer.ModelSerializer):
    '''
    '''
    pass


# == helper classes ==
class Helper:
    '''
    '''
    _registered={}

    @classmethod
    def register_serializer(cls, **kwargs):
        '''
        input
        -----
        model=serializer

        obj
        ---
        register serializer by model name
        '''
        for model_name,serializer_name in kwargs.items():
            cls._registered[model_name]=serializer_name

    @classmethod
    def toJson(cls, dbObj):
        '''
        obj
        ---
        parser grabber element wise to json

        return
        ------
        json encoded string
        '''
        model_name=dbObj.__class__.__name__.lower()
        try:
            serializerClass=cls._registered[model_name]
        except KeyError:
            msg='[-] Fail to find serializer'\
                 'for model: [{}]'.format(model_name)
            print(msg)
            return b'{"error":"serializer fail"}'
        serialized=serializerClass(dbObj)
        return JSONRenderer().render(serialized.data)

Helper.register_serializer(
    target=TargetSerializer,
    extractor=ExtractorSerializer,
    elementaction=ElementActionSerializer,
    pageaction=PageActionSerializer,
    grabber=GrabberSerializer,
    postelementaction=PostElementActionSerializer
    )
