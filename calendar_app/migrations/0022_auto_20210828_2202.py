# Generated by Django 3.1.13 on 2021-08-28 20:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0021_auto_20210828_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.time(22, 2, 23, 521715)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_start',
            field=models.TimeField(default=datetime.time(22, 2, 23, 521715)),
        ),
    ]
