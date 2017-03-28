
 #== helpers ==
def _required_fields(reqList, dataDict):
    '''
    '''
    dataset=set(dataDict.keys())
    if set(reqList).issubset(dataset):return
    msg='[-] {} are required fields'.format(', '.join(reqList))
    raise Exception(msg)

def _get_or_instance(model, lookup_field, data, serializer):
    '''
    '''
    value=data[lookup_field]
    if not value:return None
    try:
        instObj=model.objects.get(**{lookup_field:value})
    except model.DoesNotExist:
        instObj=serializer(data=data)
        if not instObj.is_valid():
            raise Exception('[-] Fail to serialized: {}'.format(value))
    print('INSTANCESSS===> {}\n'.format(type(instObj)))
    return instObj
