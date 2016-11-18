from rest_framework import serializers
from workers.models import (TaskConfig,
                            Task,
                            Job,
                            TaskProducer)
from grabbers.serializers import MapperSerializer, SequenceSerializer
from drivers.serializers import DriverSerializer
from drivers.models import Driver

from django.core.exceptions import ObjectDoesNotExist

class TaskConfigSerializer(serializers.ModelSerializer):
    '''
    '''
    driver=DriverSerializer()
    sequence=SequenceSerializer()
    class Meta:
        model=TaskConfig
        #no proxy by api yet - missing fields::proxy,network_cap
        fields=('name','driver','sequence','mapper','round_limit')

    def save(self):
        '''
        '''
        data=self.validated_data

        try:
            driver=Driver.objects.get(name=data['driver']['name'])
        except ObjectDoesNotExist:
            driverSe=DriverSerializer(data=data['driver'])




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
