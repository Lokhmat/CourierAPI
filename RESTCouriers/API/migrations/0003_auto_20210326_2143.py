# Generated by Django 3.1.7 on 2021-03-26 18:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20210326_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='regions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, null=True, size=None),
        ),
    ]