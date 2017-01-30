from django.shortcuts import render, get_object_or_404
from workers.models import Job, TaskConfig, Task
from drivers.models import Driver
from grabbers.models import Sequence
from rest_framework import viewsets, generics
from rest_framework.response import Response
from workers.serializers import (JobSerializer,
                                TaskConfigListSerializer,
                                TaskConfigDetailSerializer,
                                TaskSerializer)


# Create your views here.
class JobsViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows JOBS to be viewed or edited.
    """
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def retrieve(self, request, pk=None):
        '''
        '''
        job=Job.objects.get(pk=pk)
        jobse=JobSerializer(job)
        full_job=jobse.data
        task_sample=Task.objects.filter(job=job).first()
        task_config=task_sample.config
        task_configse=TaskConfigSerializer(task_config)
        full_job.update(task_configse.data)
        return Response(full_job)


class TaskConfigsViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows TASKCONFIGS to be viewed or edited.
    """
    queryset = TaskConfig.objects.all().order_by('id')
    serializer_class = TaskConfigListSerializer
    lookup_field='name'

    def retrieve(self, request, name=None):
        """
        """
        taskconfig = get_object_or_404(TaskConfig, name=name)
        serializer = TaskConfigDetailSerializer(taskconfig)
        return Response(serializer.data)
