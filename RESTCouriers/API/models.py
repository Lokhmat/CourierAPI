from django.db import models
from django.contrib.postgres.fields import ArrayField


class Courier(models.Model):
    courier_id = models.IntegerField(primary_key=True, unique=True)
    courier_type = models.CharField('Type of courier', max_length=4)
    regions = ArrayField(models.IntegerField(), null=True, blank=True, default=list)
    working_hours = ArrayField(models.CharField(max_length=11), null=True, blank=True, default=list)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, unique=True)
    done = models.BooleanField('Is order done already')
    weight = models.DecimalField('Weight of package', max_digits=2, decimal_places=2)
    region = models.IntegerField('Region of order')
    delivery_hours = ArrayField(models.CharField(max_length=11))
    assign_time = models.DateTimeField('Time of assignment', null=True)
    complete_time = models.DateTimeField('Time of completion', null=True)
    assigned_to = models.ForeignKey(Courier, on_delete=models.CASCADE)
