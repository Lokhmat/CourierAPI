from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Courier
import time


def is_correct_time(time_str):
    """
    Check if time string is in a correct format
    """
    try:
        time.strptime(time_str, '%H:%M')
    except ValueError:
        return False
    return len(time_str) == 5


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']

    def create(self, validated_data):
        return Courier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass

    def is_valid(self, raise_exception=True):
        """
        Validating of input data
        """
        super(CourierSerializer, self).is_valid(raise_exception=True)
        if self.initial_data['courier_id'] <= 0:
            raise ValidationError('Courier id is less that 0')
        if self.initial_data['courier_type'] not in ['foot', 'bike', 'car']:
            raise ValidationError('Courier type is not in a correct format')
        for region in self.initial_data['regions']:
            if region <= 0:
                raise ValidationError('One of regions is less that 0')
        for element in self.initial_data['working_hours']:
            if not (len(element.split('-')) == 2 and is_correct_time(element.split('-')[0]) and is_correct_time(
                    element.split('-')[1])):
                raise ValidationError('One of working hours is not in a correct format')
        return True
