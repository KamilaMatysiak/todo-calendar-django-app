# Generated by Django 3.2.6 on 2021-11-20 21:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0037_auto_20211013_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='time_end',
            field=models.TimeField(default=datetime.datetime(2021, 11, 20, 22, 45, 41, 676536)),
        ),
    ]
