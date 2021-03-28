from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Courier, Order
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
        print(str(validated_data))
        return Courier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates info about courier
        """
        # TODO: recast orders according to new Info
        instance.courier_type = self.validated_data.get('courier_type', instance.courier_type)
        instance.regions = self.validated_data.get('regions', instance.regions)
        instance.working_hours = self.validated_data.get('working_hours', instance.working_hours)
        instance.save()
        return instance

    def is_valid(self, raise_exception=True):
        """
        Validating of input data
        """

        # If we want just update model we call cascade of validate_<type>
        if self.partial:
            self.check_fields(['courier_type', 'regions', 'working_hours'])
            super(CourierSerializer, self).is_valid(raise_exception=True)
            return True
        super(CourierSerializer, self).is_valid(raise_exception=True)
        self.check_fields(['courier_type', 'courier_id', 'regions', 'working_hours'])
        if self.initial_data['courier_id'] <= 0:
            raise ValidationError('Courier id is less that 0')
        if self.initial_data['courier_type'] not in ['foot', 'bike', 'car']:
            raise ValidationError('Courier type is not in a correct format')
        for key in ['courier_id', 'courier_type', 'regions', 'working_hours']:
            if key not in self.initial_data.keys():
                raise ValidationError('{0} property is missed'.format(key))
        for region in self.initial_data['regions']:
            if region <= 0:
                raise ValidationError('One of regions is less that 0')
        for element in self.initial_data['working_hours']:
            if not (len(element.split('-')) == 2 and is_correct_time(element.split('-')[0]) and is_correct_time(
                    element.split('-')[1])):
                raise ValidationError('One of working hours is not in a correct format')
        return True

    def check_fields(self, appropriate_field):
        """
        Check if all fields in initial data are appropriate
        """
        for key in self.initial_data.keys():
            if key not in appropriate_field:
                raise ValidationError('Couriers should not have {0} property '.format(key))

    def validate_regions(self, regions):
        for region in regions:
            if region <= 0:
                raise ValidationError('One of regions is less that 0')
        return regions

    def validate_courier_type(self, courier_type):
        if courier_type not in ['foot', 'bike', 'car']:
            raise ValidationError('Courier type is not in a correct format')
        return courier_type

    def validate_working_hours(self, working_hours):
        for element in working_hours:
            if not (len(element.split('-')) == 2 and is_correct_time(element.split('-')[0]) and is_correct_time(
                    element.split('-')[1])):
                raise ValidationError('One of working hours is not in a correct format')
        return working_hours


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'weight', 'region', 'delivery_hours']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates info about courier
        """
        # TODO: recast orders according to new Info
        """
        instance.courier_type = self.validated_data.get('courier_type', instance.courier_type)
        instance.regions = self.validated_data.get('regions', instance.regions)
        instance.working_hours = self.validated_data.get('working_hours', instance.working_hours)
        instance.save()
        """
        return instance

    def is_valid(self, raise_exception=True):
        """
        Validating of input data
        """

        # TODO: update order field assigned_to

        if self.partial and len(self.initial_data) == 3:
            self.check_fields(['courier_id', 'order_id', 'complete_time'])
            super(OrderSerializer, self).is_valid(raise_exception=True)
            return True

        super(OrderSerializer, self).is_valid(raise_exception=True)
        self.check_fields(['weight', 'order_id', 'region', 'delivery_hours'])
        if self.initial_data['order_id'] <= 0:
            raise ValidationError('Order id is less that 0')
        if not 0.01 <= self.initial_data['weight'] <= 50 or not self.correct_integer(
                str(self.validated_data['weight'])):
            raise ValidationError(
                'Weight is not in a correct number gap(from 0.01 to 50) and only two digits after point')
        for key in ['weight', 'order_id', 'region', 'delivery_hours']:
            if key not in self.initial_data.keys():
                raise ValidationError('{0} property is missed'.format(key))
        if self.initial_data['region'] <= 0:
            raise ValidationError('Region is less that 0')
        for element in self.initial_data['delivery_hours']:
            if not (len(element.split('-')) == 2 and is_correct_time(element.split('-')[0]) and is_correct_time(
                    element.split('-')[1])):
                raise ValidationError('One of working hours is not in a correct format')
        return True

    def validate_complete_time(self,time):
        return time

    def check_fields(self, appropriate_field):
        """
        Check if all fields in initial data are appropriate
        """
        for key in self.initial_data.keys():
            if key not in appropriate_field:
                raise ValidationError('Order should not have {0} property '.format(key))

    def correct_integer(self, data):
        numb = data.split('.')
        if len(numb) != 1 and len(numb) != 2:
            return False
        if len(numb[1]) > 2:
            return False
        return True
