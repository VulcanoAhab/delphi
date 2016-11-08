from rest_framework import serializers
from drivers.models import Driver, Header

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
    class Meta:
        model=Driver
        fields=('name', 'type', 'headers')
