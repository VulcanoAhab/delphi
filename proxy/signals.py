
import os
import psutil
import subprocess
import signal

from django.db.models.signals import post_save
from django.dispatch import receiver
from proxy.models import Proxy
from django.conf import settings


# --------------------------------------------------------- helpers and globals
_PIDFILE=os.path.join(settings.BASE_DIR, 'proxy', 'server_pid')

def start_server(call_string):
    '''
    '''
    proc=subprocess.Popen([call_string,], shell=True)
    pid=proc.pid
    fd=open(_PIDFILE, 'w')
    fd.write(str(pid))
    fd.close()
    print('[+] Proxy server started. PID:[{}]'.format(pid))

def stop_server(pid):
    '''
    '''
    os.kill(pid, signal.SIGKILL)
    fd=open(_PIDFILE, 'w')
    fd.close()
    print('[-] Stoped proxy server. PID:[{}]'.format(pid))

# -------------------------------------------- server signals
@receiver(post_save, sender=Proxy)
def proxy_server(sender, instance, **kwargs):
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
            pid=int(pid)
            pid_on=psutil.pid_exists(pid)
    if instance.status=='on' and not pid_on:
        start_server(instance.call)
    if instance.status=='off' and pid_on:
        stop_server(pid) 


