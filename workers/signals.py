from django.db.models.signals import post_save
from django.dispatch import receiver
from workers.models import Job
from workers.tasks import job_starter
import time

@receiver(post_save, sender=Job)
def job_manager(sender, instance, **kwargs):
    '''
    '''
    if instance.status != 'created':return
    instance.status='in_queue'
    instance.save()
    time.sleep(0.1)
    job_starter.delay(instance.id)

