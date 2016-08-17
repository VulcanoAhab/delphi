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
    if not job.confs.sequence:
        print('[+] Sequence is required')
        return
    #loading vars
    url=task.target_url
    round_number=task.round_number
    control_key=build_control_key(url, job.id)
    mapper=job.confs.mapper
    sequence=job.confs.sequence.indexed_grabbers.all().order_by('sequence_index')

    #build driver
    wd=getattr(browsers, job.confs.driver.type)()
    wd.load_confs(job.confs)
    wd.build_driver()

    print('[+] Starting GET request [{}]'.format(url))
    wd.get(url)

    #process get
    ProcessSequence.set_job(job)
    ProcessSequence.set_browser(wd)
    ProcessSequence.set_sequence(sequence)
    ProcessSequence.mapping(mapper)
    ProcessSequence.run()

    wd.close()
    time_used=time.time()-init_time
    print('[+] Process took: [{0:.2f}] seconds'.format(time_used))

    #status task done
    task.status='done'
    task.save()


## ------ task manager :: provisory manager, starts tasks per job -- as pipe

@app.task
def task_manager(job_id, job_name):
    '''
    '''
    #set vars
    ask_til_three=0

    #task loop -- need to improve job control soon
    #need to be more intelligent -- maybe as periodic
    while True:

        task = Task.objects.filter(job__id=job_id, status='created').first()

        if not task:
            ask_til_three+=1
            if ask_til_three > 3:break
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
    print('[+] Starting job')
    job=Job.objects.get(pk=job_id)
    job.status='running'
    job.save()

    #test proxy
    proxy=job.confs.proxy
    if proxy and not proxy.running:
        print('[+] Proxy is set but not running...')
        exit(0)

    if job.seed:
        #create first task
        task=Task()
        task.target_url=job.seed
        task.status='created'
        task.round_number=0
        task.job=job
        task.save()
        time.sleep(1)
    task_manager.delay(job_id, job.name)
    #here will soon implement the new jobs confs for tasks
    #for example create new jobs from element(URL) XYZ

