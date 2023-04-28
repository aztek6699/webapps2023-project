# Generated by Django 4.1.7 on 2023-04-24 00:57

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_initial_admin(apps, schema_editor):
    admin = apps.get_model('base', 'CustomUser')
    admin.objects.create(
        username='admin1',
        password=make_password('admin1'),
        is_staff=True,
        is_superuser=True,
        is_active=True
    )


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_admin)
    ]
