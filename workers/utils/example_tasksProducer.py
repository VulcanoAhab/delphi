from workers.utils.tasksProducer import OneVarPagingTasks, ResultsTasks


# ----- tests

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
    #building tasks
    OneVarPagingTasks.set_job_id(job_id)
    OneVarPagingTasks.produce_tasks(base_url,
                                    paging_param,
                                    paging_range, 
                                    paging_step) 


def planalto_produce_article_tasks():
    '''
    example
    -------
    build tasks from results
    '''
    ##setting vars
    results_job_id=1
    tasks_job_id=2
    producer_fucntion=ResultsTasks.tasks_by_field('planalto_article-url')
    #building tasks
    ResultsTasks.set_results_job(results_job_id)
    ResultsTasks.set_tasks_job(tasks_job_id)
    ResultsTasks.produce_tasks(producer_fucntion)

    
