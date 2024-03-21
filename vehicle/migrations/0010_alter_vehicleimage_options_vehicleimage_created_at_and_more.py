# Generated by Django 4.2 on 2024-01-17 10:12

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0009_alter_vehicleimage_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicleimage',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.FileField(blank=True, help_text='Accepted formats: png, jpg, jpeg. Max file size 10 MB', upload_to='Vehicle_Image/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Upload Vehicle Images'),
        ),
    ]
