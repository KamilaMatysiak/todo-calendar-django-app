# Generated by Django 3.1.5 on 2021-06-14 22:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0012_auto_20210615_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date_time_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 15, 0, 37, 58, 802074)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date_time_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 15, 0, 37, 58, 802074)),
        ),
    ]
