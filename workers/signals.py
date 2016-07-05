from django.db.models.signals import post_save
from django.dispatch import receiver
from workers.models import Job
from workers.tasks import job_starter 
import time

@receiver(post_save, sender=Job)
def job_manager(sender, instance, **kwargs):
    '''
    '''
    if instance.status != 'creat':return
    instance.status='inq'
    instance.save()
    time.sleep(3)
    job_starter.delay(instance.id)

