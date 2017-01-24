from django.shortcuts import render
from rest_framework import viewsets, generics
from grabbers.serializers import SequenceSerializer
from grabbers.models import Sequence
# Create your views here.

class SequenceViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows SEQUENCE to be viewed or edited.
    """
    queryset = Sequence.objects.all().order_by('id')
    serializer_class = SequenceSerializer
