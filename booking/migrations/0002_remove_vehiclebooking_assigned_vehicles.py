# Generated by Django 4.2 on 2024-01-16 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclebooking',
            name='assigned_vehicles',
        ),
    ]
