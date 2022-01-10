# Generated by Django 3.2.6 on 2022-01-10 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_completed_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='estimated_time_interval',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='estimated_time_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='note',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
