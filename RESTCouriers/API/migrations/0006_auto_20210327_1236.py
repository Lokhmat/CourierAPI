# Generated by Django 3.1.7 on 2021-03-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20210327_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='done',
            field=models.BooleanField(default=False, verbose_name='Is order done already'),
        ),
    ]
