import time
import traceback
import psutil

from workers.models import Job
from delphi.celery import app
from drivers import browsers
from workers.models import Job, Task
from workers.utils.commons import build_control_key
from grabbers.utils.processors import ProcessSequence

#proxy
from proxy.utils.proxy import MobProxy

#django db
from django.db.utils import OperationalError, InterfaceError
from django import db
### ----- (1) helpers ----- ###





### ----- (2) power horses ----- ###

## ------ action - task : get, grab and save

@app.task
def task_run(task_id):
    '''
    '''
    # start thread
    init_time=time.time()

    #get task, set to running
    task=Task.objects.get(pk=task_id)
    task.status='running'
    task.save()

    #must have
    job=task.job
    if not task.config.sequence and not task.config.mapper:
        print('[+] Sequence or mapper must be set')
        return

    #loading vars
    wd=None
    url=task.target_url
    round_number=task.round_number
    control_key=build_control_key(url, job.id)
    mapper=task.config.mapper
    sequence=task.config.sequence
    try:
        #proxy
        MobProxy.connect(task)
        proxy_port=MobProxy.port()
        #build driver
        wd=getattr(browsers, task.config.driver.type)()
        wd.load_confs(task.config)
        wd.build_driver(proxy_port)
        print('[+] Starting GET request [{}]'.format(url))
        wd.get(url)
        #process get
        process=ProcessSequence()
        process.set_job(job)
        process.set_task(task)
        process.set_browser(wd)
        if mapper:
            process.mapping(mapper)
        elif sequence:
            indexed_seq=sequence.indexed_grabbers.all(
                           ).order_by('sequence_index')
            process.set_sequence(indexed_seq)
        else:
            raise Exception('Must set mapper or sequence')
        process.run()
        MobProxy.save_data()
        status='done'
    except Exception:
        traceback.print_exc()
        status='fail'

    if wd:
        try:
            wd.close()
        except Exception as e:
            print('[-] Fail to close browser:[{}]'.format(e))
            del wd

    time_used=time.time()-init_time
    print('[+] Process took: [{0:.2f}] seconds'.format(time_used))

    #status task done -- all this for a thread issue -- improving
    try:
        task.status=status
        task.save()
    except (OperationalError, InterfaceError):
        db.close_connection()
        task=Task.objects.get(pk=task_id)
        task.status=status
        task.save()
    return

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

        tasks = Task.objects.filter(job__id=job_id, status='created')

        if not tasks.count():
            ask_til_three+=1
            if ask_til_three > 3:break
            print('[-] No task for job [{0}]'.format(job_name))
            time.sleep(30*ask_til_three)
            continue

        for n,task in enumerate(tasks):
            if not task:continue
            print('[+] Sending task [{0}] to queue'.format(task.target_url))

            task.status='in_queue'
            task.save()
            task_run.delay(task.id)

            #update values
            ask_til_three=0
            time.sleep(0.01)
            if n % 100 ==0:
                time.sleep(30)

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

