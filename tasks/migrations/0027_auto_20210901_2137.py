# Generated by Django 3.1.13 on 2021-09-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0026_auto_20210830_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['priority', 'date', 'title', 'localization']},
        ),
        migrations.AddField(
            model_name='task',
            name='l_lat',
            field=models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='l_lon',
            field=models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=15, null=True),
        ),
    ]
