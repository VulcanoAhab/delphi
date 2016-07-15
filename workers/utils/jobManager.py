from grabbers.models import Sequence, IndexedGrabber, Grabber, Target, Extractor, PostElementAction, ElementAction, PageAction
from workers.models import JobConfig, Job, Task
from  drivers.models import Driver, Header

from django.core.exceptions import ObjectDoesNotExist

class ElementsBuilder:
    '''
    '''
    
    @classmethod
    def grabber(cls, grabber_dict):
        '''
        '''
        #set vars
        target={}
        page_action=None
        #get values
        name=grabber_dict['name']
        grabberObj, grabberCreated=Grabber.objects.get_or_create(name=name)
        if not grabberCreated: return grabberObj
        if 'target' in grabber_dict:
            target=grabber_dict['target']
        if 'page_action' in grabber_dict:
            page_action=grabber_dict['page_action'] 
        if target:
            field_name=target['field_name']
            field_selector=target['field_selector']
            selector_type=target['selector_type']
            targetObj=Target(field_name=field_name, 
                             field_selector=field_selector,
                             selector_type=selector_type)
            targetObj.save()
            grabberObj.target=targetObj
            if 'extractor' in grabber_dict:
                extractor=grabber_dict['extractor']
                exObj, exCreated=Extractor.objects.get_or_create(type=extractoO)
                grabberObj.extractor=exObj
            if 'element_action' in grabber_dict:
                action=grabber_dict['element_action']
                actionObj=Action(type=action.get('type'), name=action['name'])
            if 'post_action' in grabber_dict:
                postis=grabber_dict['post_element_action']
                name=postis['name']
                grabber_post=postis['grabber']
                grabber_post_obj=cls.grabber(grabber_post)
                grabberObj.post_action=grabber_post_obj
        if page_action:
            paType=page_action['type']
            paObj,paCreated=PageAction.objects.get_or_create(type=paType)
            grabberObj.page_action=paObj
        grabberObj.save()
        return grabberObj

    @classmethod
    def headers(cls, header_dict):
        '''
        '''
        has_headers=0
        headersObjs=[]
        if 'get' in header_dict:
            header_name=header_dict['get']
            headerObj=Header.objects.filter(header_name=header_name)
            has_headers=headerObj.count()
        if not has_headers and header_dict['set']::
            sets_name=header_dict['set']['name']
            sets=header_dict['set']['fields']
            if not sets:
                for field_name, field_value in sets.item():
                    headerObj=Header(field_name=field_name, 
                             field_value=field_value,
                             header_name=sets_name)
                    headerObj.save()
                    headersObjs.append(headerObj)
        return headerObjs

    @classmethod
    def driver(cls, name, headers={}):
        '''
        driver for now only get
        '''
        driver,created=Driver.objects.get_or_create(name=name)
        if not created: return driver
        driver.save()
        if headers:
            headerObjs=cls.headers(headers)
            for header in headerObjs:
                driver.add(header)
            driver.save()
        return driver

    @classmethod
    def sequence(cls, sequence_name=None, grabbers_list=[]):
        '''
        '''
        sequence,created=Sequence.objects.get_or_create(name=sequence_name)
        if not created:return sequence
        sequence.save()
        for grabber_dict in grabbers_list:
            index=grabber_dict['index']
            grabberObj=cls.grabber(grabber_dict)
            indexedQuery=IndexedGrabber.objects.filter(grabber=grabberObj, 
                                                               index=index)
            if not indexedQuery.count():
                indexedGrabberObj=IndexedGrabber(grabber=grabberObj, 
                                                            index=index)
            else:
                indexedGrabberObj=indexedQuery[0]
            sequence.indexedGrabber=indexedGrabberObj
        return sequence
    
    @classmethod
    def mapper(cls, mapper_dict):
        '''
        '''
        name=mapper_dict['name']
        mapperObj, mapperCreated=Mapper.objects.get_or_create(name=name)
        if not mapperCreated: return mapperObj
        field_name=['field_name']
        field_selector['field_selector']
        mapperObj.field_name=field_name
        mapperObj.field_selector=field_selector
        if 'page_action' in  mapper_dict:
            page_action=mapper_dict['page_action']
            paType=page_action['type']
            paObj,paCreated=PageAction.objects.get_or_create(type=paType)
            mapperObj.page_action=paObj 
        mapperObj.save()
        return mapperObj

class JobBuilder:
    '''
    '''
    def __init__(self, jobDict):
        '''
        '''
        self.jobDict=jobDict
    
    def create_job(self):
        '''
        '''
        jobDict=self.jobDict
        job_name=jobDict['name']
        try:
            jobObj=Job.objects.get(name=job_name)
            raise Exception('Job Already Exist')
        except ObjectDoesNotExist:
            pass 
        #jobConfig first try
        jobConfig_name=jobDict['job_config']['name']
        try:
            jobConfigObj=JobConfig.objects.get(name=jobConfig_name)
        except ObjectDoesNotExist:
            #driver
            driver_name=jobDict['driver']['name']
            headers=jobDict['driver']['headers']
            driverObj=ElementsBuilder.driver(driver_name, headers=headers)
            #sequence
            sequence=jobDict['sequence']
            sequence_name=sequence['name']
            grabbers=sequence['grabbers']
            sequenceObj=ElementsBuilder.sequence(sequence_name, grabbers)
            #mapper
            mapperObj=None
            if 'mapper' in jobDict:
                mapper=jobDict['mapper']
                mapperObj=ElementsBuilder.mapper(mapper)
            #----- jobconfig 
            jobConfigObj=JobConfig(
                name=jobConfig_name,
                sequence=sequenceObj,
                driver=driverObj,
                mapper=mapperObj
                )
            jobConfigObj.save()
        #----- job
        jobObj=Job(name=job_name, 
                   seed=jobDict['seed'],
                   status=jobDict['status'],
                   confs=jobConfigObj)
        jobObj.save()
        print('[+] Job was created.')

