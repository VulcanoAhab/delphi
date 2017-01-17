from django.db.models.signals import post_save
from django.dispatch import receiver
from workers.models import Job, TaskProducer, Task
# from workers.tasks import job_starter
import time

# @receiver(post_save, sender=Job)
# def job_manager(sender, instance, **kwargs):
#     '''
#     '''
#     if instance.status != 'created':return
#     instance.status='in_queue'
#     instance.save()
#     time.sleep(0.1)
#     job_starter.delay(instance.id)


@receiver(post_save, sender=TaskProducer)
def build_tasks(sender, instance, **kwards):
    '''
    '''
    if instance.status != 'created':return
    instance.status='running'
    instance.save()
    time.sleep(0.1)
    for url in instance.urls_list.split(','):
        if not url:continue
        url=url.strip()
        task=Task()
        task.job=instance.job
        task.status='created'
        task.config=instance.task_config
        task.target_url=url
        task.save()
        time.sleep(0.001) #a little rhythm
    instance.status='done'
    instance.save()
