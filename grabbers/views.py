from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from grabbers.serializers import SequenceSerializer, MapperSerializer
from grabbers.models import Sequence, Mapper
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class SequenceViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows SEQUENCE to be viewed or edited.
    """
    queryset = Sequence.objects.all().order_by('-id')
    serializer_class = SequenceSerializer
    lookup_field='name'

    def retrieve(self, request, name=None):
        """
        """
        seq = get_object_or_404(Sequence, name=name)
        serializer = SequenceSerializer(seq)
        return Response(serializer.data)

    def create(self, request):
        '''
        '''
        seqse=SequenceSerializer(data=request.data)
        if seqse.is_valid():
            seqse.save()
            return Response(seqse.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                seqse.errors, status=status.HTTP_400_BAD_REQUEST)


class MapperViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows SEQUENCE to be viewed or edited.
    """
    queryset = Mapper.objects.all().order_by('id')
    serializer_class = MapperSerializer
    lookup_field='name'

    def retrieve(self, request, name=None):
        """
        """
        mapis = get_object_or_404(Mapper, name=name)
        serializer = MapperSerializer(mapis)
        return Response(serializer.data)
