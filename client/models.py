from django.db import models
from django.core.validators import RegexValidator,FileExtensionValidator

allowed_image_extensions = ['png','jpg','jpeg','pdf']
PHONE_NUMBER_REGEX = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Only valid Phone Number is required')

class Client(models.Model):
    company_name = models.CharField(max_length=100,verbose_name="Company Name")
    company_email = models.EmailField(max_length=100,verbose_name="Company Email")
    company_phone = models.CharField(max_length=18,verbose_name="Company Phone Number",validators=[PHONE_NUMBER_REGEX])
    address = models.CharField(max_length=255,verbose_name="Address")
    license = models.FileField(
                    upload_to="client/", 
                    help_text="Accepted formats: png, jpg, jpeg , pdf. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)], 
                    verbose_name="License")
    focal_person_name = models.CharField(max_length=100,verbose_name="Focal Person Name")
    phone_number = models.CharField(max_length=20,verbose_name="Phone Number",validators=[PHONE_NUMBER_REGEX])
    email = models.EmailField(max_length=100,verbose_name="Email",blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['-created_at']  
      