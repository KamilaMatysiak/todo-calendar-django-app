# Generated by Django 3.1.13 on 2021-08-30 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0034_merge_20210829_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date_end',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date_start',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_start',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]