# Generated by Django 4.2 on 2024-01-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='owner',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
