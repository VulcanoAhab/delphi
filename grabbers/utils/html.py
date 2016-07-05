import collections
import copy
import tempfile
from lxml import html

#django
from django.core.files import File

#db models
from urlocators.models import Page, Locator, make_url_id
from information.models import PageData
from workers.models import Job


## ---  build extractors dict
class BuildEx:
    '''
    '''
    
    _work_dict={}
    
    @classmethod
    def clean_work_dict(cls):
        '''
        '''
        cls._work_dict={}

    @classmethod
    def get_work_dict(cls):
        '''
        '''
        return copy.deepcopy(cls._work_dict)
           
    
    @classmethod
    def build_work(cls, targets, post_act=None):
        '''
        '''
        from grabbers.models import Target, Action, PostActTarget, Extractor
        

        for target in targets:
            
            #set target vars
            tname=target.field_name
            tselector=target.field_selector
            tselector_type=target.selector_type
            tid=target.id
            tdict={}
            tdict[tname]={'selector':tselector, 
                          'selector_type':tselector_type}
            if post_act is not None:
                post_act.update(tdict)
            
            #build attrs list
            atquery=Extractor.objects.filter(target=tid)
            attrs=[e.attr for e in atquery]
            tdict[tname].update({'attrs':attrs})
            
            #build action dicts 
            ac_query=Action.objects.filter(target=tid).order_by('index')
            actions=[]
            if not ac_query.count():
                tdict[tname].update({'actions':actions})
                if post_act is None:
                    cls._work_dict.update(tdict)
                continue
            for action in ac_query:
                ac_name=action.name
                acdict={
                    'name':ac_name, 
                    'type':action.type, 
                    'index': action.index, 
                    'post_act':{}
                        }
                #test if post act targets
                apquery=PostActTarget.objects.filter(act=action.id)
                if not apquery.count():
                    actions.append(ac_dict)    
                    continue
                #chain actions - recursive call
                cls.build_work(apquery, acdict['post_act'])
                actions.append(acdict)
            tdict[tname].update({'actions':actions})
            
            ##update work dict
            cls._work_dict.update(tdict)


    @classmethod
    def asDict(cls, grabber):
        '''
        '''
        from grabbers.models import Target
        targets=Target.objects.filter(grabber=grabber)
        cls.build_work(targets)


## ---  find & grab page data
class Grabis:
    '''
    pagesource data interface
    for now just a simple wrappper
    '''
    @staticmethod
    def _exData(field_name, htmlElement, attrs):
        '''
        '''
        datum=[]
        for ats in attrs:
            if ats == 'text':
                datum.append(htmlElement.text)
            else:
                datum.append(htmlElement.attrib.get(ats))
        return datum
    
    @staticmethod
    def load_data_from_selected(elements, field, attrs):
        '''
        '''
        data_container=[dict() for _ in elements]
        for n,value in enumerate(elements):
            data=Grabis._exData(field, value, attrs)
            data_container[n].update({field:data})
        return data_container
     
    @staticmethod
    def load_page(browser, selectors, eltype='xpath', parent_dict={}, only_load=False):
        '''
        '''
        parent=None
        hit_round=0
        #wait for elements
        for s in selectors:
            browser.wait_for_element(s, eltype=eltype)
        
        if only_load:return

        source=browser.page_source
        url=browser.current_url
        url_id=make_url_id(url)
        
        if parent_dict:
            hit_round=parent_dict['round']+1
            parent=parent_dict['id']
        
        source_dict={
                'source':source,
                'url':url,
                'parent':parent,
                'round':hit_round,
                'id':url_id,
                    }
        
        return source_dict, html.fromstring(source)
    
    def __init__(self):
        '''
        '''
        #work containers
        self._page_object=None
        self._selector=None
        #result containers
        self.data=[]
        self.page_source={}

    
    def set_selector(self, selector):
        '''
        '''
        self._selector=selector
        #cls.eltype=cls._geteltype(selector)
        #will be implemented soon - for now, only xptah
        self._eltype='xpath' 
    
    def set_page_object(self, page_object):
        '''
        '''
        self._page_object=page_object
    
    def get_data(self, field_name, attrs):
        '''
        '''
        return Grabis.load_data_from_selected(self.data, field_name, attrs)

    def grab(self):
        '''
        '''
        self.data=getattr(self._page_object, self._eltype)(self._selector)
        
            
    def act(self, browser, field_name, config_dict):
        '''
        for now -- to simplify development 
        and fisrts test, only one action and no chaining in 
        post_action
        '''
        
        field_confs=config_dict[field_name]
        action_len=len(field_confs['actions'])
        if action_len > 1:
            print('[+] Warning: Only considering one action is this version')
        elif action_len <= 0:
            return
        
        #do a generic call in browser class - selenium and others wrapper
        act_list=browser.browser.find_elements_by_xpath(self._selector)
        act_list_range=range(len(act_list)) #i know, but...

        action=field_confs['actions'][0] #for now only one action per act -- lets make simple
        action_type=action['type']
        action_name=action['name']
        post_act=action['post_act']
        
        post_container=[] 
        #action and possible grab data
        for index in act_list_range:
            
            if index >= len(act_list)-1:break

            element=act_list[index]
            getattr(element, action_type)() #always a function
            
            #only one post_act and no chaining yet
            post_items=list(post_act.items())
            if len(post_items)>1:
                print('[+] Warning: Only one post_action in this version')
            post_field_name, post_conf=post_items[0]
            selector=post_conf['selector'] or None
            
            page_source,page_object=Grabis.load_page(browser, [selector,])
            
            gb=Grabis()
            gb.set_page_object(page_object)
            gb.set_selector(selector)
            #------ need to ad page source to result here

            attrs=post_conf['attrs']
            if not attrs:continue

            gb.grab()
            click_list=gb.get_data(field_name, attrs)
            post_container.append({'html':page_source, 'target_data':click_list}) 
            
            #do a generic call in browser class - selenium and others wrapper
            browser.browser.back()
            Grabis.load_page(browser, [self._selector,], only_load=True)
            act_list=browser.browser.find_elements_by_xpath(self._selector)
        
        return post_container

## ---  extract page data
class Pythoness:
    '''
    '''
    _extractis={}
    _data={
        'page_source':[],
        'page_data':[],
          }
    _job=None
    
    @classmethod
    def set_job(cls, job):
        '''
        '''
        cls._job=job

    @classmethod
    def set_fields(cls, **kwargs):
        '''
        '''
        cls._extractis={k:v for k,v in kwargs.items()}
        print('[+] Setting extractors [{0}]'.format(cls._extractis))

    @classmethod
    def session(cls, browser):
        '''
        '''
        # set base values
        fields=list(cls._extractis.keys())
        elements_lists=[]
        
        #nasty but trying to guarantee all elements | need improvement soon
        selectors=[cls._extractis[f]['selector'] for f in fields]
        page_source,page_object=Grabis.load_page(browser,selectors)
        cls._data['page_source'].append(page_source)

        for f in fields:
            selector=cls._extractis[f]['selector']
            gb=Grabis()
            gb.set_selector(selector)
            gb.set_page_object(page_object)
            
            if cls._extractis[f]['actions']:
                data=gb.act(browser,f, cls._extractis)
                cls._data['page_data'].extend(data)
            elif cls._extractis[f]['attrs']:
                gb.grab() 
                data=gb.get_data(f, cls._extractis[f]['attrs'])
                data={'html':page_source, 'target_data':data}
                cls._data['page_data'].append(data)
       

    @classmethod
    def save_data(cls):
        '''
        '''
        for page in cls._data['page_data']:
            
            page_source=page['html']['source']
            page_url=page['html']['url']
            page_url_id=page['html']['id']
            
            page_data=page['target_data']

            locs, created=Locator.objects.get_or_create(url_id=page_url_id)
            if created:
                locs.url=page_url
                locs.save()

            page,created=Page.objects.get_or_create(url=locs)
            if created:
                fp=tempfile.TemporaryFile()
                fp.write(page_source.encode())
                fp.seek(0)
                page.html=File(fp)
                page.job.add(cls._job)
                page.url=locs
                page.save()
                
                #close temp file
                fp.close()
    
                
            for dict_item in page_data:
                for field_name, values in dict_item.items():
                    for value in values:
                        if not value:continue
                        pd=PageData()
                        pd.field_name=field_name
                        pd.field_value=value
                        pd.page=page
                        pd.save()
            
            
            
class ProcessPage:
    '''
    '''
    _exdict={}
    _browser=None
    _job_id=None

    @classmethod
    def set_job_id(cls, job_id):
        '''
        '''
        cls._job_id=job_id

    @classmethod
    def set_target_fields(cls, grabber):
        '''
        '''
        print('[+] Grabber [{}] running.'.format(grabber))
        BuildEx.clean_work_dict()
        BuildEx.asDict(grabber)
        cls._exdict=BuildEx.get_work_dict()
    
    @classmethod
    def set_browser(cls, browser):
        '''
        '''
        cls._browser=browser

    @classmethod
    def process_grabber(cls):
        '''
        '''
        job=Job.objects.get(id=cls._job_id)
        Pythoness.set_job(job)
        Pythoness.set_fields(**cls._exdict)
        Pythoness.session(cls._browser)
        Pythoness.save_data()

