# Generated by Django 3.1.13 on 2021-08-30 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0025_merge_20210829_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['priority', 'date']},
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('N', '---'), ('L', 'Niski'), ('M', 'Średni'), ('H', 'Wysoki')], default='N', max_length=10),
        ),
    ]
