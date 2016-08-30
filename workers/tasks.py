import time
import traceback
import psutil

from workers.models import Job
from delphi.celery import app
from drivers import browsers
from workers.models import Job, Task
from workers.utils.commons import build_control_key
from grabbers.utils.processors import ProcessSequence

### ----- (1) helpers ----- ###





### ----- (2) power horses ----- ###

## ------ action - task : get, grab and save

@app.task
def task_run(task_id):
    '''
    '''

    init_time=time.time()

    #must have
    task=Task.objects.get(pk=task_id)
    job=task.job
    if not task.config.sequence and not task.config.mapper:
        print('[+] Sequence or mapper must be set')
        return
    #loading vars
    url=task.target_url
    round_number=task.round_number
    control_key=build_control_key(url, job.id)
    mapper=task.config.mapper
    sequence=task.config.sequence

    #test proxy
    proxy=task.config.proxy
    if proxy and not proxy.running:
        print('[+] Proxy is set but not running...')
        exit(0)


    #build driver
    try:

        wd=getattr(browsers, task.config.driver.type)()
        wd.load_confs(task.config)
        wd.build_driver()

        if proxy:
            #prepare for get
            pass

        print('[+] Starting GET request [{}]'.format(url))
        wd.get(url)

        #process get
        ProcessSequence.set_job(job)
        ProcessSequence.set_browser(wd)
        if mapper:
            ProcessSequence.mapping(mapper)
        elif sequence:
            indexed_seq=sequence.indexed_grabbers.all(
                           ).order_by('sequence_index')
            ProcessSequence.set_sequence(indexed_seq)
        else:
            raise Exception('Must set mapper or sequence')
        ProcessSequence.run()
        #pass proxy to data collection ----
        status='done'
    except Exception as e:
        print('[-] Exception on task level', e)
        status='fail'

    wd.close()
    time_used=time.time()-init_time
    print('[+] Process took: [{0:.2f}] seconds'.format(time_used))

    #status task done
    task.status=status
    task.save()


## ------ task manager :: provisory manager, starts tasks per job -- as pipe

@app.task
def task_manager(job_id, job_name):
    '''
    '''
    #set vars
    ask_til_three=0
    #wait for task to be saved - just in case
    time.sleep(1)
    #task loop -- need to improve job control soon
    #need to be more intelligent -- maybe as periodic
    while True:

        task = Task.objects.filter(job__id=job_id, status='created').first()

        if not task:
            ask_til_three+=1
            if ask_til_three > 3:
                #test for running tasks
                while True:
                    task_running = Task.objects.filter(job__id=job_id, status='running')
                    running_count=task_running.count()
                    if not running_count():break
                    print('[+] Waiting runnning tasks: [{}]'.format(running_count()))
                    time.spleep(5)
                break
            print('[-] No task for job [{0}]'.format(job_name))
            time.sleep(30*ask_til_three)
            continue

        print('[+] Starting task [{0}]'.format(task.target_url))

        task.status='running'
        task.save()
        task_run.delay(task.id)
        task=None
        ask_til_three=0

    print('[+] Done all tasks for job [{0}]'.format(job_name))


## ------ task starts job - creates first task - fires task manager

@app.task
def job_starter(job_id=1):
    '''
    '''
    job=Job.objects.get(pk=job_id)
    print('[+] Starting job [{}]'.format(job.name))
    job.status='running'
    job.save()
    task_manager.delay(job_id, job.name)

