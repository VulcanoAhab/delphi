
###################################################################
###################################################################
class GrabberConf:
    '''
    '''
    @classmethod
    def toDict(cls, grabberObj):
        '''
        '''
        #set var
        work_dict={}

        #helper function - recursion
        def post_helper(grabberObj):
            '''
            '''
            if not grabberObj.post_action:return {}
            return grabberObj.post_action.grabber

        #dict build
        if grabberObj.target:
            target_selector=grabberObj.target.field_selector
            target_name=grabberObj.target.field_name
            target_selector_type=grabberObj.target.selector_type
            tempDict={}
            tempDict['selector']=target_selector
            tempDict['name']=target_name
            tempDict['selector_type']=target_selector_type
            work_dict['target']=tempDict
        if grabberObj.extractor:
            work_dict['extractors']=[grabberObj.extractor.type]
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
        task_config_name=mapper.task_config.name
        task_dict={
            'name':field_name,
            'selector':field_selector,
            'task_config_name':task_config_name,
               }
        return task_dict

