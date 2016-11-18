from collections import namedtuple
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

    def save(self):
        '''
        '''
        field_name=self.self.validated_data.pop('field_name')
        target,created=Target.objects.get_or_create(field_name=field_name)
        if created:
            for k,v in self.validated_data.items():
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
    '''
    post_action not available (yet) through serializer
    '''
    target=TargetSerializer(allow_null=True,required=False)
    extractors=ExtractorSerializer(allow_null=True,required=False)
    element_action=ElementActionSerializer(allow_null=True, required=False)
    page_action=PageActionSerializer(allow_null=True, required=False)
    name=serializers.CharField(max_length=250)

    class Meta:
        model=Grabber
        fields=('name','extractors', 'element_action',
                'page_action', 'target',
                'created_at', 'last_modified')


    def save(self):
        '''
        '''
        _fields={
            'element_action':None,
            'page_action':None,
            'extractors':None,
            'target':None,
                }
        #build related objects
        try:
            grab_name=self.validated_data.pop('name')
        except KeyError as key:
            msg='[-] The {} field is required'.format(key)
            print(msg)
            raise Exception(msg)

        if self.validated_data.get('extractors'):
            extype=self.validated_data['extractors']['type']
            (_fields['extractors'],
            created)=Extractor.objects.get_or_create(type=extype)

        if self.validated_data.get('target'):
            tar_name=self.validated_data['target']['field_name']
            (_fields['target'],
            created)=Target.objects.get_or_create(field_name=tar_name)
            if created:
                _fields['target'].field_selector=target['field_selector']
                _fields['target'].selector_type=target['selector_type']
                _fields['target'].save(commit=False)

        if self.validated_data.get('element_action'):
            el=self.self.validated_data['element_action']['type']
            (_fields['element_action'],
            created)=ElementAction.objetcs.get_or_create(type=el)

        if self.validated_data.get('page_action'):
            pa=self.self.validated_data['page_action']['type']
            (_fields['page_action'],
            created)=PageAction.objects.get_or_create(type=pa)

        grabber, grab_created=Grabber.objects.get_or_create(name=grab_name)

        if grab_created:
            for k,v in _fields.items():
                if not v:continue
                setattr(grabber, k, v)
            grabber.save()

        return grabber

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

    def save(self):
        '''
        '''
        name=self.validated_data['name']
        sequence,created=Sequence.objects.get_or_create(name=name)
        if not created:return

        for indexed_grabber in self.validated_data['indexed_grabbers']:

            grabis_index=indexed_grabber['sequence_index']
            grabis_name=indexed_grabber['grabber']['name']

            if IndexedGrabber.objects.filter(
                sequence_index=grabis_index,
                grabber=grabis_name).exists():continue

            grabber=Grabber.objects.filter(name=grabis_name).first()
            if not grabber:
                grabis=GrabberSerializer(data=indexed_grabber['grabber'])
                if not grabis.is_valid():
                    msg='[-] Fail top parse grabber {}'.format(grabis_name)
                    raise TypeError(msg)
                grabber=grabis.save()

            indexGrabbis=IndexedGrabber(sequence_index=grabis_index,
                                        grabber=grabber)
            indexGrabbis.save()
            sequence.indexed_grabbers.add(indexGrabbis)
