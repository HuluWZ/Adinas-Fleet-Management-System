# Generated by Django 4.2 on 2024-01-18 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0010_alter_vehicleimage_options_vehicleimage_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.FileField(help_text='Accepted formats: png, jpg, jpeg. Max file size 10 MB', upload_to='vehicle_image/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Upload Vehicle Images'),
        ),
    ]
