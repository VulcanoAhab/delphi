import time
import traceback
import psutil

from datetime import timedelta
from workers.models import Job
from delphi.celery import app
from drivers import browsers
from workers.models import Job, Task, RunControl
from workers.utils.commons import build_control_key
from grabbers.utils.processors import ProcessSequence

#proxy
from proxy.utils.proxy import MobProxy

#django db
from django.db.utils import OperationalError, InterfaceError
from django import db

#celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task

### ----- (1) tasks ----- ###
@periodic_task(run_every=(timedelta(seconds=3)))
def task_run():
    '''
    '''
    #one more try
    #db.close_old_connections()

    #get task, set to running
    task_in=Task.objects.filter(status='wait').first()
    if not task_in:
        print('[+] No tasks in wait')
        return
    task_in.status='running'
    task_in.save()

    # start thread
    init_time=time.time()

    #must have
    job=task_in.job
    if not task_in.config.sequence and not task_in.config.mapper:
        print('[+] Sequence or mapper must be set')
        return

    #loading vars
    wd=None
    url=task_in.target_url
    round_number=task_in.round_number
    control_key=build_control_key(url, job.id)
    mapper=task_in.config.mapper
    sequence=task_in.config.sequence
    try:
        #proxy
        MobProxy.connect(task_in)
        proxy_port=MobProxy.port()
        #build driver
        wd=getattr(browsers, task_in.config.driver.type)()
        wd.load_confs(task_in.config)
        wd.build_driver(proxy_port=proxy_port)
        print('[+] Starting GET request [{}]'.format(url))
        wd.get(url)
        #process get
        process=ProcessSequence()
        process.set_job(job)
        process.set_task(task_in)
        process.set_target_url(url)
        process.set_browser(wd)
        if mapper:
            process.mapping(mapper)
        elif sequence:
            process.set_sequence(sequence)
        else:
            raise Exception('Must set mapper or sequence')
        process.run()
        MobProxy.save_data()
        status='done'
        job.tasks_done_count+=1
        job.save()
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
    task_in.status=status
    task_in.save()
    return

### ----- (2) jobs ----- ###
@periodic_task(run_every=(crontab(minute="*/5")))
def jobs_run():
    '''
    '''
    tasks_ceiling=150
    run_control=RunControl()
    while True:
        jobs=Job.objects.filter(status__in=['created', 'running'])
        jobs_count=jobs.count()
        if not jobs_count:
            print('[+] No new jobs and no jobs running')
            if run_control.ask_count <= 3:
                time.sleep(30*run_control.run_count)
                run_control.ask_count+=1
                continue
            break
        #ask renew
        run_control.ask_count=0
        #soon will consider tasks duration
        tasks_limit=100
        taskal=tasks_ceiling/jobs_count
        if taskal >  1:
            tasks_limit=taskal
        for job in jobs:
            tasks=Task.objects.filter(job=job, status='created')
            tasks_count=tasks.count()
            #new job
            if job.status=='created':
                print("[+] Starting job {}.\
                Total tasks: {}".format(job.name, tasks_count))
                job.status='running'
                job.save()
            #done job
            if not tasks_count:
                if job.done_count >= 2:
                    job.status='done'
                    job.save()
                    print('[+] Job {} is done'.format(job.name))
                    continue
                job.done_count+=1
                job.save()
                time.sleep(0.01)
                continue
            #run task
            for task in tasks[:tasks_limit]:
                task.status='wait'
                task.save()
                time.sleep(0.01)
