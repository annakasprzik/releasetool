# Generated by Django 2.0.9 on 2018-10-08 15:36

from django.db import migrations
from django.contrib.auth import get_user_model


def empty_config(apps, schema_editor):
    user_model = get_user_model()
    if not user_model.objects.filter(username='rtadmin').exists():
        user_model.objects.create_superuser('rtadmin', 'admin@example.com', 'changeme')

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('zaptain_rt_app', '0002_initial_data')
    ]

    operations = [
        migrations.RunPython(empty_config)
    ]
