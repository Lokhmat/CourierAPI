# Generated by Django 3.1.7 on 2021-03-28 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_auto_20210328_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='earnings',
            field=models.IntegerField(default=0, verbose_name='Earnings of a courier'),
        ),
    ]
