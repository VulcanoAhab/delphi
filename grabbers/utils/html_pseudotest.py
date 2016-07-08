import time
import traceback

from workers.models import Job
from drivers import browsers
from workers.models import Job, Task
from workers.utils.commons import build_control_key
from grabbers.utils.processors import ProcessSequence

def test_process(task_id=18):
    '''
    '''

    init_time=time.time()

    #set vars
    task=Task.objects.get(pk=task_id)
    job=task.job
    url=task.target_url
    round_number=task.round_number
    control_key=build_control_key(url, job.id)
    mapper=job.confs.mapper
    if not job.confs.sequence:
        print('[+] Sequence is required')
        return
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

    time_used=time.time()-init_time
    print('[+] Process took: [{0:.2f}] seconds'.format(time_used))
