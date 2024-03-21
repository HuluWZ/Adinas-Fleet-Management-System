from datetime import date
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from client.models import Client
from vehicle.models import VehicleBrand, VehicleModel, VehicleType, VehicleData

allowed_image_extensions = ["png", "jpg", "jpeg"]
allowed_file_extensions = ["png", "jpg", "jpeg", "pdf"]

# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=200)
    booking = models.IntegerField(default=12)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["-created_at"]

class VehicleBooking(models.Model):
    client_info = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Client Info"
    )
    pickup = models.CharField(max_length=100, verbose_name="Pick Up Location")
    drop_off = models.CharField(max_length=100, verbose_name="Drop Off Location")
    daily_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Daily Price",
    )
    no_of_vehicles = models.IntegerField(default=1, verbose_name="Number Of Vehicles")
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.CASCADE, verbose_name="Vehicle Type", default=1
    )
    brand = models.ForeignKey(
        VehicleBrand,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Make",
    )
    model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Model",
    )
    production_year = models.IntegerField(
        validators=[
            MaxValueValidator(
                timezone.now().year, message="Production year cannot be in the future."
            )
        ],
        null=True,
        blank=True,
        verbose_name="Production Year",
    )
    start_date = models.DateField(
        verbose_name="Start Date",
        default=date.today,
    )
    end_date = models.DateField(
        verbose_name="End Date",
        default=date.today,
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1, message="Duration must be at least 1 day")]
    )
    remark = models.CharField(max_length=100,verbose_name="Remark if any",default="")
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.client_info

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
      if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date")
      if not self.pk: # only run on create
          if self.start_date < date.today():
              raise MinValueValidator("Start Date can't be before today")
          if self.end_date < date.today():
              raise MinValueValidator("End Date can't be before today")
          

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)


class AssignedVehicle(models.Model):
    vehicle_request = models.ForeignKey(
        VehicleBooking, on_delete=models.CASCADE, related_name="assigned"
    )
    vehicle = models.ForeignKey(
        VehicleData, on_delete=models.CASCADE, related_name="assigned"
    )
    is_active = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation before saving
        super().save(*args, **kwargs)
