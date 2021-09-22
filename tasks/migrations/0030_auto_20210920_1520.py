# Generated by Django 3.1.13 on 2021-09-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0029_merge_20210919_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('N', '---'), ('L', 'Niski'), ('J', 'Średni'), ('H', 'Wysoki')], default='N', max_length=10),
        ),
    ]