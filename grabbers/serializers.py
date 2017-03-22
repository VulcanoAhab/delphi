from collections import namedtuple
from rest_framework import serializers
from grabbers.models import (Target,
                             Extractor,
                             ElementAction,
                             PageAction,
                             PostElementAction,
                             Grabber,
                             Mapper,
                             Sequence,
                             IndexedGrabber)
# == helpers ==
def _required_fields(reqList, dataDict):
    '''
    '''
    dataset=set(dataDict.keys())
    if set(reqList).issubset(dataset):return
    msg='[-] {} are required fields'.format(', '.join(reqList))
    raise Exception(msg)

def _get_or_instance(model, lookup_field, data):
    '''
    '''
    value=data.pop(lookup_field)
    if not value:return None
    try:
        instObj=model.objects.get(**{lookup_field:value})
    except model.DoesNotExist:
        instObj=model()
        for k,v in data.items():
            setattr(instObj,k,v)
    return instObj

# == Serializers Models ==
class TargetSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Target
        fields=('field_name', 'field_selector', 'selector_type',
                'created_at', 'last_modified')

    def to_internal_value(self, data):
        '''
        '''
        reqs=('field_name', 'field_selector', 'selector_type')
        _required_fields(reqs, data)
        return data

    def save(self):
        '''
        '''
        fname=self.validated_data.pop('field_name')
        target,created=Target.objects.get_or_create(field_name=fname)
        if created:
            for k,v in self.validated_data.items():
                setattr(target, k,v)
            target.save()
        return target


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

    def create(self, validated_data):
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
            grab_name=validated_data.pop('name')
        except KeyError as key:
            msg='[-] The {} field is required'.format(key)
            raise Exception(msg)
        if validated_data.get('extractors'):
            _fields['extractors']=_get_or_instance(Extractor,'type',
                                            validated_data['extractors'])
        if validated_data.get('target'):
            _fields['target']=_get_or_instance(Target, 'field_name',
                                                validated_data['target'])
        if validated_data.get('element_action'):
            _fields['element_action']=_get_or_instance(ElementAction, 'type',
                                            validated_data['element_action'])
        if validated_data.get('page_action'):
            _fields['page_action']=_get_or_instance(PageAction,'type',
                                                validated_data['page_action'])
        grabber=Grabber.objects.filter(name=grab_name).first()
        if not grabber:
            grabber=Grabber()
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
        fields='__all__'

    def to_representation(self, obj):
        '''
        '''
        name=obj.name
        sequence=Sequence.objects.get(name=name)
        value_fields=['name','element_action','post_action',
                      'created_at', 'last_modified']
        seqs={'name':name, 'indexed_grabbers':[]}
        for indexed_grabber in obj.indexed_grabbers.all():
            grabber_index=indexed_grabber.sequence_index
            grabber=Grabber.objects.get(id=indexed_grabber.grabber.id)
            if not grabber:continue
            grabis={field:getattr(grabber, field) for field in  value_fields}
            grabis.update({
                'grabber':{
                    'name':grabber.name,
                    'extractors':ExtractorSerializer(grabber.extractor).data,
                    'target':TargetSerializer(grabber.target).data,
                          },
                'sequence_index':grabber_index,
            })
            seqs['indexed_grabbers'].append(grabis)
        sorted(seqs['indexed_grabbers'], key=lambda o:o['sequence_index'])
        #return {'data':seqs}
        return seqs


    def create(self, validated_data):
        '''
        '''
        name=validated_data['name']
        sequence,created=Sequence.objects.get_or_create(name=name)
        if not created:
            print("[-] We already this guy in db")
            return sequence
        for indexed_grabber in validated_data['indexed_grabbers']:
            grabis_index=indexed_grabber['sequence_index']
            grabis_name=indexed_grabber['grabber']['name']
            grabber=Grabber.objects.filter(name=grabis_name).first()
            if not grabber:
                grabis=GrabberSerializer(data=indexed_grabber['grabber'])
                if not grabis.is_valid():
                    msg='[-] Fail top parse grabber {}'.format(grabis_name)
                    raise TypeError(msg)
                grabber.save()
            indexGrabbis=IndexedGrabber.objects.filter(
                sequence_index=grabis_index, grabber=grabber).first()
            if not indexGrabbis:
                indexGrabbis=IndexedGrabber(sequence_index=grabis_index,
                                        grabber=grabber)
                #many to many needs to be saved
                indexGrabbis.save()
            sequence.indexed_grabbers.add(indexGrabbis)
        return sequence
