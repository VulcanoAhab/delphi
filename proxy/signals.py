
import os
import psutil
import subprocess
import signal

from django.db.models.signals import post_save
from django.dispatch import receiver
from proxy.models import Proxy
from django.conf import settings


#--------------------------------------------------------- helpers and globals
_PIDFILE=os.path.join([settings.BASE_DIR, 'proxy', 'server_pid')





@receiver(post_save, sender=Proxy)
def job_manager(sender, instance, **kwargs):
    '''
    '''
    pid=None
    pid_on=False
    has_pid=os.path.exists(_PIDFILE)
    if has_pid:
        fd=open(_PIDFILE, 'r')
        pid=fd.read().strip()
        fd.close()
        if pid:
            pid_on=psutil.pid_exists(pid)
    if instance.status=='on' and not pid_on:
        start_server(instance.call)
    if instance.status=='off' and pid_on:
        os.kill(pid, signal.SIGKILL)



