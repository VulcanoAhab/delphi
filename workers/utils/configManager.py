from rest_framework.renderers import JSONRenderer

from grabbers.serializers import (  TargetSerializer,
                                    ExtractorSerializer,
                                    ElementActionSerializer,
                                    PageActionSerializer,
                                    GrabberSerializer,
                                    PostElementActionSerializer,
                                    MapperSerializer,
                                    IndexedGrabberSerializer,
                                    SequenceSerializer)

from workers.serializers import (   TaskConfigSerializer,
                                    TaskSerializer,
                                    JobSerializer )


# --- render objs ---
class Renderer:
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


Renderer.register_serializer(
    target=TargetSerializer,
    extractor=ExtractorSerializer,
    elementaction=ElementActionSerializer,
    pageaction=PageActionSerializer,
    grabber=GrabberSerializer,
    postelementaction=PostElementActionSerializer,
    mapper=MapperSerializer,
    indexedgrabber=IndexedGrabberSerializer,
    sequence=SequenceSerializer,
    taskconfig=TaskConfigSerializer,
    task=TaskSerializer,
    job=JobSerializer
    )
