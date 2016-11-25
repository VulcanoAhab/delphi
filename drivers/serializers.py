from rest_framework import serializers
from drivers.models import Driver, Header
from django.core.exceptions import ObjectDoesNotExist


class HeaderSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Header
        fields=('field_name', 'field_value', 'header_name')

class DriverSerializer(serializers.ModelSerializer):
    '''
    '''
    headers=HeaderSerializer(many=True)
    name=serializers.CharField(max_length=250)

    class Meta:
        model=Driver
        fields=('name', 'type', 'headers')

    def save(self):
        '''
        '''
