from rest_framework import serializers
from workers.models import (TaskConfig,
                            Task,
                            Job,
                            TaskProducer)
from grabbers.serializers import (MapperSerializer,
                                  SequenceSerializer)
from grabbers.models import Sequence
from drivers.serializers import DriverSerializer
from drivers.models import Driver
from django.core.exceptions import ObjectDoesNotExist
# == helpers ==
from delphi.utils.lizers import _required_fields, _get_or_instance


class TaskConfigDetailSerializer(serializers.ModelSerializer):
    '''
    '''
    driver=DriverSerializer()
    sequence=SequenceSerializer()

    class Meta:
        model=TaskConfig
        #no proxy by api yet - missing fields::proxy,network_cap
        fields=('name','driver','sequence','mapper','round_limit')

    def create(self, validated_data):
        '''
        '''
        name=validated_data['name']

        try:
            task_config=TaskConfig.objects.get(name=name)
            print("[-] We already this guy in db")
            return task_config
        except TaskConfig.DoesNotExist:
            task_config=TaskConfig(name=name)

        driver=_get_or_instance(Driver,'name',
                                validated_data['driver'],DriverSerializer)
        sequence=_get_or_instance(Sequence,'name',
                                  validated_data['sequence'],
                                  SequenceSerializer)
        task_config.driver=driver
        task_config.sequence=sequence
        return task_config

class TaskConfigListSerializer(serializers.HyperlinkedModelSerializer):
    '''
    '''
    class Meta:
        model=TaskConfig
        fields=('url', 'name', 'sequence', 'driver', 'mapper','round_limit')
        extra_kwargs = {
            'url': {'view_name': 'api:task_config-detail', 'lookup_field':'name'},
            'driver': {'view_name': 'api:driver-detail', 'lookup_field':'name'},
            'sequence':{'view_name': 'api:sequence-detail', 'lookup_field':'name'},
            'mapper':{'view_name':'api:mapper-detail', 'lookup_field':'name'},
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
