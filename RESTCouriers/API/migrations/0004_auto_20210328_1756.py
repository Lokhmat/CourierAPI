# Generated by Django 3.1.7 on 2021-03-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20210328_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='assign_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time of assignment'),
        ),
    ]
