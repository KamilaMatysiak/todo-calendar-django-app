# Generated by Django 3.1.13 on 2021-08-28 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_auto_20210827_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date(2021, 8, 28), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.TimeField(default=datetime.time(22, 1, 1, 993140)),
        ),
    ]
