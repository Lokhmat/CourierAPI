from django.db import models
from django.contrib.postgres.fields import ArrayField


class Courier(models.Model):
    courier_id = models.IntegerField(primary_key=True, unique=True)
    courier_type = models.CharField('Type of courier', max_length=4)
    regions = ArrayField(models.IntegerField(), blank=True, default=list)
    working_hours = ArrayField(models.CharField(max_length=11), blank=True, default=list)
    earnings = models.IntegerField('Earnings of a courier', default=0)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, unique=True)
    done = models.BooleanField('Is order done already', default=False)
    weight = models.FloatField('Weight of package')
    region = models.IntegerField('Region of order')
    delivery_hours = ArrayField(models.CharField(max_length=11))
    assign_time = models.DateTimeField('Time of assignment', null=True)
    complete_time = models.DateTimeField('Time of completion', null=True)
    assigned_to = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True)
