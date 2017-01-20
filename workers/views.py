from django.shortcuts import render
from workers.models import Job,TaskConfig
from workers.serializers import JobSerializer, TaskConfigSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response


# Create your views here.
class JobsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def retrieve(self, request, pk=None):
        '''
        '''
        pass
