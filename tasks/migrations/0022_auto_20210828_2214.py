# Generated by Django 3.1.13 on 2021-08-28 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0021_auto_20210828_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]