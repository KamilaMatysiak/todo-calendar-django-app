# Generated by Django 3.1.5 on 2021-06-15 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0014_auto_20210615_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date_time_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 15, 17, 13, 18, 366191)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date_time_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 15, 17, 13, 18, 366191)),
        ),
    ]
