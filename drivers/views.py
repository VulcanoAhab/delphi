from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from drivers.serializers import DriverSerializer
from drivers.models import Driver
from rest_framework.response import Response


# Create your views here.

class DriverViewSet(viewsets.ModelViewSet):
    """
    """
    queryset=Driver.objects.all()
    serializer_class=DriverSerializer
    lookup_field='name'

    def retrieve(self, request, name=None):
        """
        """
        dr = get_object_or_404(Driver, name=name)
        serializer = DriverSerializer(dr)
        return Response(serializer.data)
