# Generated by Django 4.2 on 2024-01-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_vehiclebooking_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclebooking',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
