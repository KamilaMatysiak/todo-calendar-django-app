# Generated by Django 3.2.2 on 2021-06-14 23:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0009_auto_20210615_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date_end',
            field=models.DateField(default=datetime.date(2021, 6, 15)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.time(1, 11, 1, 275613)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_start',
            field=models.TimeField(default=datetime.time(1, 11, 1, 275613)),
        ),
    ]