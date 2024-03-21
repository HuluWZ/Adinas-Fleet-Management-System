from django.db import models
from django.utils import timezone
from django.core.validators import (
    RegexValidator,
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from accounts.models import UserAccount
from django.db.models.signals import pre_delete
from django.dispatch import receiver


allowed_image_extensions = ["png", "jpg", "jpeg"]
allowed_file_extensions = ["png", "jpg", "jpeg", "pdf"]
PHONE_NUMBER_REGEX = RegexValidator(
    r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$",
    "Only valid Phone Number is required",
)

class AreaOfInterest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class VehicleType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class VehicleModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class VehicleBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class VehicleColor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class VehicleData(models.Model):
    account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="vehicle"
    )
    plate_number = models.CharField(max_length=100, unique=True, verbose_name="Plate Number")
    area_of_interests = models.ManyToManyField(AreaOfInterest,related_name="vehicle",blank=True)
    address = models.CharField(max_length=100, verbose_name="City")
    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.CASCADE,
        verbose_name="Vehicle Type",
        related_name="vehicle",
    )
    libre = models.FileField(
        upload_to="vehicle/",
        help_text="Accepted formats: png, jpg, jpeg, pdf. Max file size 10 MB",
        validators=[FileExtensionValidator(allowed_extensions=allowed_file_extensions)],
        blank=True,
        verbose_name="Libre",
    )
    license = models.FileField(
        upload_to="vehicle/",
        help_text="Accepted formats: png, jpg, jpeg, pdf. Max file size 10 MB",
        validators=[FileExtensionValidator(allowed_extensions=allowed_file_extensions)],
        blank=True,
        verbose_name="License",
    )
    color = models.ForeignKey(
        VehicleColor,
        on_delete=models.CASCADE,
        verbose_name="Color",
        related_name="vehicle",
    )
    brand = models.ForeignKey(
        VehicleBrand,
        on_delete=models.CASCADE,
        verbose_name="Vehicle Make",
        related_name="vehicle",
    )
    model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        verbose_name="Model",
        related_name="vehicle",
    )
    transmission = models.CharField(
        choices=(
            ("", "Select Transmission"),
            ("Manual", "Manual"),
            ("Automatic", "Automatic"),
        ),
        max_length=50,
    )
    fuel_type = models.CharField(
        choices=(
            ("", "Select Fuel Type"),
            ("Diesel / ናፍጣ", "Diesel / ናፍጣ"),
            ("Benzene / ቤንዚል", "Benzene / ቤንዚል"),
        ),
        null=True,
        blank=True,
        max_length=50,
    )
    driver_status = models.CharField(
        choices=(
            ("", "Select Driver Status"),
            ("With Driver", "With Driver"),
            ("With Out Driver", "With Out Driver"),
        ),
        max_length=100,
    )
    production_year = models.IntegerField(
        validators=[
            MaxValueValidator(
                timezone.now().year, message="Production year cannot be in the future."
            )
        ],
        verbose_name="Production Year",
    )
    price_per_day = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Price Per Day",
    )
    is_active = models.BooleanField(default=True)
    is_ontrip = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.SET_NULL, 
        related_name="vehicle_created_by",
        null=True
    )
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.plate_number

    class Meta:
        ordering = ["-created_at"]


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        VehicleData, on_delete=models.CASCADE, related_name="images"
    )
    image = models.FileField(
        upload_to="vehicle_image/",
        verbose_name="Vehicle Image",
        help_text="Accepted formats: png, jpg, jpeg",
        blank=False,
        validators=[
            FileExtensionValidator(allowed_extensions=allowed_image_extensions)
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


@receiver(pre_delete, sender=VehicleData)
def delete_vehicle_images(sender, instance, **kwargs):
    instance.images.all().delete()
