from django.db import models

# Create your models here.

_status=[
    ('inq', 'in_queue'), #conf loaded - all ok to go
    ('creat', 'created'), #just created job
    ('done','done'),
    ('on','running')
        ]

class JobConfig(models.Model):
    '''
    '''
    name=models.CharField(max_length=150)
    driver=models.ForeignKey('drivers.Driver')
    sequence=models.ForeignKey('grabbers.Sequence')
    mapper=models.ForeignKey('grabbers.Mapper')

    def __str__(self):
        '''
        '''
        return self.name

class Job(models.Model):
    '''
    '''
    confs=models.ForeignKey('workers.JobConfig')
    seed=models.URLField(max_length=500)
    status=models.CharField(max_length=5, choices=_status)
    results_count=models.IntegerField(default=0)
    round_limit=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=150, unique=True)

    def __str__(self):
        return '{}<|>{}'.format(self.seed.url, self.confs.name)

class Task(models.Model):
    '''
    '''
    target_url=models.URLField(max_length=750)
    status=models.CharField(max_length=5, choices=_status)
    type=models.CharField(max_length=150, default='request')
    round_number=models.IntegerField()
    job=models.ForeignKey('workers.Job')
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        '''
        return ':::'.join([self.target_url, str(self.round_number)])


