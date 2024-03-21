# Generated by Django 4.2 on 2024-01-17 08:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0008_alter_vehicleimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.FileField(blank=True, help_text='Accepted formats: png, jpg, jpeg. Max file size 10 MB', upload_to='Vehicle Image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Upload Vehicle Images'),
        ),
    ]
