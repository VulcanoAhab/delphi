from workers.utils.jobManager import JobBuilder
import json

jobDict= {
    "name":"moviePageData",
    "seed":"http://www.imdb.com/title/tt0079944/?ref_=fn_al_tt_1",
    "status":"created",
    
    "job_config":{"name":"moviePageData"},

    "driver":{
        "name":"leanMachine_eng",
        "headers":{
                "set":{}, 
                "get":"firefox_mac",
                    },
            },
    
    "sequence":{
        "name":"moviePageData",
        "grabbers":[
            {
            "name":"MovieTitle",
            "target":{
                "field_name":"title",
                "field_selector":".//head/title",
                "selector_type":"xpath",
                        },
            "extractor":{
                "type":"text_content",
                        },
            "index":0,                
            "element_action":{},
            "post_action":{},
            "page_action":"",
            },]},
}


def dict2job(jobDict=jobDict):
    '''
    '''
    jb=JobBuilder(jobDict)
    jb.create_job()
