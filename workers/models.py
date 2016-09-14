from django.db import models

# Create your models here.

_status=[
    ('in_queue', 'in_queue'), #conf loaded - all ok to go
    ('created', 'created'), #just created job
    ('done','done'),
    ('running','running'),
    ('fail','fail'),
    ('to_approve','to_approve'),
        ]

class TaskConfig(models.Model):
    '''
    '''
    name=models.CharField(max_length=150, unique=True)
    driver=models.ForeignKey('drivers.Driver')
    sequence=models.ForeignKey('grabbers.Sequence', blank=True, null=True)
    mapper=models.ForeignKey('grabbers.Mapper', blank=True, null=True)
    proxy=models.ForeignKey('proxy.Proxy', blank=True, null=True)
    network_cap=models.BooleanField(default=False)
    round_limit=models.IntegerField(default=0)

    def __str__(self):
        '''
        '''
        return self.name

class Job(models.Model):
    '''
    '''
    status=models.CharField(max_length=50, choices=_status)
    results_count=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=150, unique=True)

    def __str__(self):
        return 'id:[{}]name:[{}]'.format(self.id, self.name)

class Task(models.Model):
    '''
    '''
    target_url=models.URLField(max_length=750)
    config=models.ForeignKey('workers.TaskConfig')
    status=models.CharField(max_length=50, choices=_status)
    type=models.CharField(max_length=150, default='request')
    round_number=models.IntegerField(default=0)
    job=models.ForeignKey('workers.Job')
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return 'url:[{}]id:[{}]'.format(self.target_url, str(self.id))


class MapperProducer(models.Model):
    '''
    '''
    urls_list=models.TextField()
    job=models.ForeignKey('workers.Job')
    status=models.CharField(max_length=50, choices=_status)
    task_config=models.ForeignKey('workers.TaskConfig')
    type=models.CharField(max_length=150, default='request')
    round_number=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return 'jobMapper:[{}]'.format(self.job.name)
