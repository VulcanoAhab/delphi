
from functools import partial


class Model:
    '''
    '''

    fields=[]

    @staticmethod
    def getis(attr, instance):
        '''
        '''
        if attr not in instance._obj:return None
        return instance._obj[attr]

    @staticmethod
    def setis(attr, value, instance):
        '''
        '''
        if attr not in instance.fields:
            raise AttributeError('[-] Unkown field: {}'.format(attr))
        instance._obj[attr]=value

    def __init__(self, **kwargs, obj={}):
        '''
        '''
        if kwargs:
            obj.update(kwargs)
        if obj:self._test_fields(obj)
        self._obj=obj
        #set properties
        for field in self._fields:
            getfn=partial(Model.getis, field)
            setfn=partial(Model.setis, field)
            setattr(Model, field, property(getfn, setfn))

    def _test_fields(self, obj):
        '''
        '''
        obj_set=set(obj.keys())
        fields_set=set(self.fields)
        test_fields=obj_set.issubset(fields_set)
        if test_fields:return
        unkwon=' ,'.join(obj_set.difference(fields_set))
        raise AttributeError('[-] Unkown fields: {}'.format(unkwon))

    @property
    def asDict(self):
        '''
        '''
        return self._obj
