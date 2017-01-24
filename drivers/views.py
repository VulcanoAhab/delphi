from django.shortcuts import render
from rest_framework import viewsets, generics
from drivers.serializers import DriverSerializer
from drivers.models import Driver

# Create your views here.

class DriverViewSet(viewsets.ModelViewSet):
    """
    """
    queryset=Driver.objects.all()
    serializer_class=DriverSerializer
