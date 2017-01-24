from rest_framework import serializers
from workers.models import (TaskConfig,
                            Task,
                            Job,
                            TaskProducer)

from grabbers.serializers import (MapperSerializer,
                                  SequenceSerializer)


from drivers.serializers import DriverSerializer
from drivers.models import Driver

from django.core.exceptions import ObjectDoesNotExist

class TaskConfigDetailSerializer(serializers.ModelSerializer):
    '''
    '''
    driver=DriverSerializer()
    sequence=SequenceSerializer()
    class Meta:
        model=TaskConfig
        #no proxy by api yet - missing fields::proxy,network_cap
        fields=('name','driver','sequence','mapper','round_limit')

class TaskConfigListSerializer(serializers.HyperlinkedModelSerializer):
    '''
    '''
    class Meta:
        model=TaskConfig
        fields=('url', 'name', 'sequence', 'driver', 'mapper','round_limit')
        extra_kwargs = {
            'url': {'view_name': 'api:task_config-detail'},
            'driver': {'view_name': 'api:driver-detail'},
            'sequence':{'view_name': 'api:sequence-detail'},
            'mapper':{'view_name':'api:mapper-detail'},
        }


class JobSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Job
        fields=('status','name')

class TaskSerializer(serializers.ModelSerializer):
    '''
    '''
    config=TaskConfigDetailSerializer()
    job=JobSerializer()
    class Meta:
        model=Task
        fields=('target_url', 'config', 'status', 'job')
