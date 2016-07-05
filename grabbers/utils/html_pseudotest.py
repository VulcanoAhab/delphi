import time
import traceback

from workers.models import Job
from drivers import browsers
from workers.models import Job, Task
from workers.utils.commons import build_control_key
from grabbers.utils.html import ProcessPage

def test_process(task_id=18):
    '''
    '''
    
    task=Task.objects.get(pk=task_id)
    job=task.job
    url=task.target_url
    round_number=task.round_number
    control_key=build_control_key(url, job.id)
    sequence=job.confs.sequence
    
    #no more talk, lets work
    wd=getattr(browsers, job.confs.driver.type)()
    wd.load_confs(job.confs)
    wd.build_driver()
    print('[+] Starting GET RESQUEST [{}]'.format(url))
    wd.get(url)
    for grabber in sequence.grabbers.all().order_by('sequence_index'):
        
        ProcessPage.set_job_id(job.id)
        print('[+] Setting targets for grabber [{0}]'.format(grabber.name))
        ProcessPage.set_target_fields(grabber)
        print('[+] Setting browser for grabber [{0}]'.format(grabber.name))
        ProcessPage.set_browser(wd)
        print('[+] Processing page')
        ProcessPage.process_grabber()


