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
        #test if exists
        grabberQuery=Grabber.objects.filter(name=name)
        if grabberQuery.count():
            #return most recent
            return grabberQuery[0]
        #build obj
        grabberObj=Grabber()
        grabberObj.name=name
        if 'target' in grabber_dict:
            target=grabber_dict['target']
        if 'page_action' in grabber_dict:
            page_action=grabber_dict['page_action']
        if target:
            field_name=target['field_name']
            field_selector=target['field_selector']
            selector_type=target['selector_type']
            #soon create a hash field for that
            targetObjQuery=Target.objects.filter(field_name=field_name,
                                                field_selector=field_selector,
                                                selector_type=selector_type)
            if targetObjQuery.count():
                targetObj=targetObjQuery[0]
            else:
                targetObj=Target(field_name=field_name,
                                 field_selector=field_selector,
                                 selector_type=selector_type)
                targetObj.save()
            grabberObj.target=targetObj
            if ('element_action' in grabber_dict
                and grabber_dict['element_action']):
                action=grabber_dict['element_action']
                actionObj=ElementAction(type=action.get('type'),
                                        name=action['name'])
            if ('post_action' in grabber_dict
                and grabber_dict['post_action']):
                postis=grabber_dict['post_action']
                name=postis['name']
                grabber_post=postis['grabber']
                grabber_post_obj=cls.grabber(grabber_post)
                grabberObj.post_action=grabber_post_obj
            #if something fails::problem of saving grabber before time
            if 'extractors' in grabber_dict:
                grabberObj.save()
                extractors=grabber_dict['extractors']
                for extractor in extractors:
                    exObj, exCreated=Extractor.objects.get_or_create(
                                                type=extractor['type'])
                    if exCreated: exObj.save()
                    grabberObj.extractors.add(exObj)
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
        if 'get' in header_dict and header_dict['get']:
            header_name=header_dict['get']
            headerObjsQuery=Header.objects.filter(header_name=header_name)
            has_headers=headerObjsQuery.count()
            if has_headers:
                headersObjs=list(headerObjsQuery)
        if not has_headers and header_dict['set']:
            header_name=header_dict['set']['name']
            sets=header_dict['set']['fields']
            if sets:
                for field_name, field_value in sets.items():
                    headerQuery=Header.objects.filter(header_name=header_name,
                                                      field_name=field_name)
                    if headerQuery.count():
                        headerObj=headerQuery[0] #for now get teh most recent
                    else:
                        headerObj=Header(field_name=field_name,
                                         field_value=field_value,
                                         header_name=header_name)
                        headerObj.save()
                    headersObjs.append(headerObj)
        return headersObjs

    @classmethod
    def driver(cls, name, driver_type=None, headers={}):
        '''
        driver for now only get
        '''
        driver,created=Driver.objects.get_or_create(name=name)
        if not created and not driver_type and not headers: return driver
        if driver_type:
            driver.type=driver_type
        if headers:
            if created:driver.save()
            headerObjs=cls.headers(headers)
            for header in headerObjs:
                driver.headers.add(header)
        driver.save()
        return driver

    @classmethod
    def sequence(cls, sequence_name=None, grabbers_list=[]):
        '''
        '''
        sequence=None
        sequenceQuery=Sequence.objects.filter(name=sequence_name)
        if sequenceQuery.count():
            return sequenceQuery[0]
        sequence=Sequence()
        sequence.name=sequence_name
        #for many to many adds::newd to delete in fail
        sequence.save()
        try:
            for grabber_dict in grabbers_list:
                index=grabber_dict['index']
                grabberObj=cls.grabber(grabber_dict)
                indexedQuery=IndexedGrabber.objects.filter(grabber=grabberObj,
                                                           sequence_index=index)
                if not indexedQuery.count():
                    indexedGrabberObj=IndexedGrabber(grabber=grabberObj,
                                                     sequence_index=index)
                    indexedGrabberObj.save()
                else:
                    indexedGrabberObj=indexedQuery[0]
                sequence.indexed_grabbers.add(indexedGrabberObj)
            sequence.save()
            return sequence
        except Exception as e:
            if sequence: sequence.delete()
            raise Exception(e)

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
            driver_type=jobDict['driver'].get('type', None)
            headers=jobDict['driver'].get('headers', {})
            driverObj=ElementsBuilder.driver(driver_name, driver_type, headers=headers)
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

