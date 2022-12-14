# Generated by Django 3.2.6 on 2022-01-13 20:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('date_start', models.DateField(default=datetime.datetime.now)),
                ('time_start', models.TimeField(default=datetime.datetime.now)),
                ('date_end', models.DateField(default=datetime.datetime.now)),
                ('time_end', models.TimeField(default=datetime.datetime.now)),
                ('color', models.CharField(default='blue', max_length=50)),
                ('cyclical', models.CharField(blank=True, max_length=20, null=True)),
                ('is_cyclical', models.BooleanField(default=False)),
                ('cycle_interval', models.CharField(blank=True, max_length=10, null=True)),
                ('cycle_number', models.IntegerField(blank=True, null=True)),
                ('with_who', models.CharField(max_length=200, null=True)),
                ('localization', models.CharField(max_length=200, null=True)),
                ('l_lat', models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=15, null=True)),
                ('l_lon', models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=15, null=True)),
                ('user', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_start', 'time_start', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=250, null=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendar_app.meeting')),
                ('user', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
