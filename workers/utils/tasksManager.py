import time
from workers.models import Task, Job
from workers.tasks import task_manager

def build_task(url, job):
    '''
    '''
    tk=Task(target_url=url, job=job, status='created')
    tk.save()

def createFromFile(file_path, job_id):
    '''
    '''
    job=Job.objects.get(pk=job_id)
    fd=open(file_path, 'r')
    tasks_urls=set([f.strip('\n').strip() for f in fd.readlines()])
    fd.close()
    for url in tasks_urls:
        build_task(url, job)
        time.sleep(0.1)

def run_created_tasks(job_id, name):
    '''
    '''
    task_manager.delay(job_id, name)
