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
        extra_kwargs = {'url': {'view_name': 'api:driver-detail'}}

    def save(self):
        '''
        '''
        data=self.validated_data
        name=data['name']

        try:
            driver=Driver.objects.get(name=name)
        except ObjectDoesNotExist:
            driver=Driver()
            driver.name=name
            driver.type=data['type']
            driver.save()
            if data.get('headers'):
                for header in data['headers']:
                    headerObj,created=Header.objects.get_or_create(
                                                            **header)
                    if created:
                        headerObj.save()
                    driver.headers.add(headerObj)
            driver.save()
        return driver
