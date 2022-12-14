# Generated by Django 3.2.6 on 2022-01-13 20:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tasks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendar_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('user', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('localization', models.CharField(max_length=200)),
                ('l_lat', models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=15, null=True)),
                ('l_lon', models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=15, null=True)),
                ('with_who', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today, null=True)),
                ('time', models.TimeField(default=datetime.datetime.now)),
                ('priority', models.CharField(choices=[('N', '---'), ('L', 'Niski'), ('J', 'Średni'), ('H', 'Wysoki')], default='N', max_length=10)),
                ('complete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('accepted', models.BooleanField(default=True)),
                ('is_cyclical', models.BooleanField(default=False)),
                ('cycle_interval', models.CharField(blank=True, max_length=10, null=True)),
                ('cycle_number', models.IntegerField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=300, null=True)),
                ('estimated_time_number', models.CharField(blank=True, max_length=3, null=True)),
                ('estimated_time_interval', models.CharField(blank=True, max_length=10, null=True)),
                ('category', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.category')),
                ('from_who', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, validators=[tasks.models.temporary_user_validation])),
                ('meeting', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_app.meeting')),
                ('user', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['complete', 'priority', 'date', 'title', 'localization'],
            },
        ),
    ]
