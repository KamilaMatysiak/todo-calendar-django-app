# Generated by Django 3.1.13 on 2021-08-28 20:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_auto_20210828_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.TimeField(default=datetime.time(22, 2, 34, 83048)),
        ),
    ]
