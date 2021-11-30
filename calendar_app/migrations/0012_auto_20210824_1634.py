# Generated by Django 3.1.7 on 2021-08-24 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0011_auto_20210822_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date_end',
            field=models.DateField(default=datetime.date(2021, 8, 24)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date_start',
            field=models.DateField(default=datetime.date(2021, 8, 24)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.time(14, 34, 16, 569100)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_start',
            field=models.TimeField(default=datetime.time(14, 34, 16, 569100)),
        ),
    ]
