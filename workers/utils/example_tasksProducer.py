from workers.utils.tasksProducer import OneVarPagingTasks, ResultsTasks


# ----- tasks by paging
def produce_byPaging(job_id, base_url, config_name,
                     paging_param,paging_range, paging_step):
    '''
    '''
    #building tasks
    OneVarPagingTasks.set_job_id(job_id)
    OneVarPaging.set_config_name(config_name)
    OneVarPagingTasks.produce_tasks(base_url,
                                    paging_param,
                                    paging_range,
                                    paging_step)

def planalto_pre_article():
    '''
    example
    -------
    build tasks by mounting paging urls
    '''
    ##setting vars
    job_id=1
    base_url='http://www2.planalto.gov.br/acompanhe-o-planalto/discursos#b_start='
    paging_param='b_start'
    paging_step=20
    paging_range=(20,980)
    config_name='planalto-paging'
    produce_byPaging(job_id,
                     base_url,
                     config_name,
                     paging_param,
                     paging_range,
                     paging_step)


#----- task by results
def produce_byResults(results_job_id, tasks_job_id, target_field, config_name):
    '''
    '''
    #building tasks
    ResultsTasks.set_results_job(results_job_id)
    ResultsTasks.set_tasks_job(tasks_job_id)
    ResultsTasks.set_config_name(config_name)
    producer_fucntion=ResultsTasks.tasks_by_field(target_field)
    ResultsTasks.produce_tasks(producer_fucntion)

def planalto_produce_article_tasks():
    '''
    example
    -------
    build tasks from results
    '''
    ##setting vars
    results_job_id=1
    tasks_job_id=2
    target_field='planalto_article-url'
    config_name='planalto_article-config'
    produce_byResults(results_job_id,
                      tasks_job_id,
                      target_field,
                      config_name)
