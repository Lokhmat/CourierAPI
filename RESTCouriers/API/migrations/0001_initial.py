# Generated by Django 3.1.7 on 2021-03-27 10:12

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('courier_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('courier_type', models.CharField(max_length=4, verbose_name='Type of courier')),
                ('regions', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('working_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=11), blank=True, default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('done', models.BooleanField(default=False, verbose_name='Is order done already')),
                ('weight', models.FloatField(verbose_name='Weight of package')),
                ('region', models.IntegerField(verbose_name='Region of order')),
                ('delivery_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=11), size=None)),
                ('assign_time', models.DateTimeField(null=True, verbose_name='Time of assignment')),
                ('complete_time', models.DateTimeField(null=True, verbose_name='Time of completion')),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API.courier')),
            ],
        ),
    ]
