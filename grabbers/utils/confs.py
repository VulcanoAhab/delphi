
###################################################################
###################################################################
class GrabberConf:
    '''
    '''

    @classmethod
    def toDict(cls, grabberObj):
        '''
        '''
        work_dict={}
        def post_helper(grabberObj):
            '''
            '''
            if not grabberObj.post_action:return {}
            return cls.toDict(grabberObj)
        if grabberObj.target:
            target_selector=grabberObj.target.field_selector
            target_name=grabberObj.target.field_name
            target_selector_type=grabberObj.target.selector_type
            tempDict={}
            tempDict['selector']=target_selector
            tempDict['name']=target_name
            tempDict['selector_type']=target_selector_type
            work_dict['target']=tempDict
        extis=grabberObj.extractors.all()
        if extis.count():
            work_dict['extractors']=[e.type for e in extis]
        if grabberObj.element_action:
            work_dict['element_action']=grabberObj.element_action.type
        if grabberObj.page_action:
            work_dict['page_action']=grabberObj.page_action.type
        work_dict['post_action']=post_helper(grabberObj)
        return work_dict

###################################################################
###################################################################
class MapperConf:
    '''
    '''
    @classmethod
    def toDict(cls, mapper):
        '''
        '''
        field_name=mapper.field_name
        field_selector=mapper.field_selector
        return {'name':field_name, 'selector':field_selector}

