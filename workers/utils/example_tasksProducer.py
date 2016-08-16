from workers.utils.tasksProducer import OneVarPagingTasks


# ----- tests

def planalto_pre_article():
    '''
    '''
    job_id=1
    base_url='http://www2.planalto.gov.br/acompanhe-o-planalto/discursos#b_start='
    paging_param='b_start'
    paging_step=20
    paging_range=(20,980)
    OneVarPagingTasks.set_job_id(job_id)
    OneVarPagingTasks.produce_tasks(base_url,
                                    paging_param,
                                    paging_range, 
                                    paging_step) 
