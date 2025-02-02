# Generated by Django 4.2 on 2024-01-16 20:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0005_alter_vehicledata_brand_alter_vehicledata_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicledata',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.FileField(blank=True, help_text='Accepted formats: png, jpg, jpeg. Max file size 10 MB', upload_to='Vehicle Image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Upload Vehicle Images'),
        ),
    ]
