from rest_framework import serializers
from workers.models import (TaskConfig,
                            Task,
                            Job,
                            TaskProducer)
from grabbers.serializers import MapperSerializer, SequenceSerializer
from drivers.serializers import DriverSerializer

class TaskConfigSerializer(serializers.ModelSerializer):
    '''
    '''
    driver=DriverSerializer()
    sequence=SequenceSerializer()
    class Meta:
        model=TaskConfig
        #no proxy by api yet - missing fields::proxy,network_cap
        fields=('name','driver','sequence','mapper','round_limit')


class JobSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Job
        fields=('status','name')

class TaskSerializer(serializers.ModelSerializer):
    '''
    '''
    config=TaskConfigSerializer()
    job=JobSerializer()
    class Meta:
        model=Task
        fields=('target_url', 'config', 'status', 'job')
