# Generated by Django 3.2.6 on 2022-01-13 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='PL')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='static/image/avatars/', verbose_name='profile picture')),
                ('avatar_thumb', models.ImageField(blank=True, null=True, upload_to='static/image/avatars/thumbs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
