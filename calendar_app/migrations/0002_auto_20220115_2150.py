# Generated by Django 3.2.6 on 2022-01-15 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='cycle_interval',
            field=models.CharField(default='d', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='cycle_number',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
