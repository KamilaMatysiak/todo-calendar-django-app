# Generated by Django 3.1.13 on 2021-08-10 20:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20210810_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='time',
            field=models.TimeField(default=datetime.time(22, 23, 58, 298672)),
        ),
    ]