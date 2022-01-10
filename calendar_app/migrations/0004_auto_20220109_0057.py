# Generated by Django 3.2.6 on 2022-01-08 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0003_auto_20211215_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='cycle_interval',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='cycle_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='cyclical',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='is_cyclical',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]