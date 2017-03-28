from rest_framework import serializers
from drivers.models import Driver, Header
from django.core.exceptions import ObjectDoesNotExist


class HeaderSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model=Header
        fields=('field_name', 'field_value', 'header_name')

    def create(self, validated_data):
        '''
        '''
        field_name=validated_data['field_name']
        header_name=validated_data['header_name']
        try:
            header=Header.objects.get(field_name=field_name,
                                       header_name=header_name)
        except ObjectDoesNotExist:
            header=Header(**validated_data)
        return header


class DriverSerializer(serializers.ModelSerializer):
    '''
    '''
    headers=HeaderSerializer(many=True)
    name=serializers.CharField(max_length=250)

    class Meta:
        model=Driver
        fields=('name', 'type', 'headers')

    def create(self, validated_data):
        '''
        '''
        name=validated_data['name']
        try:
            driver=Driver.objects.get(name=name)
        except ObjectDoesNotExist:
            driver=Driver()
            driver.name=name
            driver.type=data['type']
            if data.get('headers'):
                for header in data['headers']:
                    headerObj,created=Header.objects.get_or_create(
                                                            **header)
                    if created:headerObj.save()
                    driver.headers.add(headerObj)
        return driver
