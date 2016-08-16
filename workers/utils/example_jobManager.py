from workers.utils.jobManager import JobBuilder
import json

jobDict= {
    "name":"moviePageData",
    "seed":"http://www.imdb.com/title/tt0079944/?ref_=fn_al_tt_1",
    "status":"created",

    "job_config":{"name":"moviePageData"},

    "driver":{
        "name":"leanMachine_eng",
        "type":"LeanRequests",
        "headers":{
            "set":{
                'name':'titlepage_firefox_mac_en',
                'fields':{
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language':'en',
                    'Accept-Encoding':'gzip, deflate, br',
                    'Connection':'keep-alive',
                        },
                    },

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
            "extractors":[
                {"type":"text_content"},
                        ],
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
