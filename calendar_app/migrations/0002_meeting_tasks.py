# Generated by Django 3.2.6 on 2021-11-24 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('calendar_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='tasks',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.task'),
        ),
    ]