# Generated by Django 2.2.24 on 2021-11-22 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0038_meeting_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ['date_start', 'time_start', 'title']},
        ),
    ]
