from django.db import models

# Create your models here.

_status=[
    ('in_queue', 'in_queue'), #conf loaded - all ok to go
    ('created', 'created'), #just created job
    ('done','done'),
    ('running','running'),
    ('to_approve','to_approve'),
        ]

class JobConfig(models.Model):
    '''
    '''
    name=models.CharField(max_length=150)
    driver=models.ForeignKey('drivers.Driver')
    sequence=models.ForeignKey('grabbers.Sequence')
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
    confs=models.ForeignKey('workers.JobConfig')
    seed=models.URLField(max_length=500, null=True, blank=True)
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
    status=models.CharField(max_length=50, choices=_status)
    type=models.CharField(max_length=150, default='request')
    round_number=models.IntegerField(default=0)
    job=models.ForeignKey('workers.Job')
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return 'url:({})id:({})'.format(self.target_url, str(self.id))


