# Generated by Django 3.1.7 on 2021-08-25 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0014_auto_20210825_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.time(18, 30, 55, 733472)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_start',
            field=models.TimeField(default=datetime.time(18, 30, 55, 733472)),
        ),
    ]