# Generated by Django 3.1.13 on 2021-08-16 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0008_auto_20210816_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.time(20, 20, 13, 424794)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_start',
            field=models.TimeField(default=datetime.time(20, 20, 13, 424794)),
        ),
    ]
