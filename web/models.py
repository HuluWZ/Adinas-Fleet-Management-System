from django.db import models
from django.core.validators import FileExtensionValidator , RegexValidator

allowed_image_extensions = ['png','jpg','jpeg']
PHONE_NUMBER_REGEX = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Only valid Phone Number is required')

class Message(models.Model):
    name = models.CharField(max_length=100,verbose_name="Name")
    email = models.EmailField(verbose_name="Email Address")
    phone_number = models.CharField(max_length=20,validators=[PHONE_NUMBER_REGEX])
    note = models.TextField(verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name="Title")
    description = models.TextField(null=True, blank=True,verbose_name="Description")
    image = models.ImageField(upload_to='content/',
                    help_text="Accepted formats: png, jpg, jpeg. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)],verbose_name="Slider Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='content/',
                    help_text="Accepted formats: png, jpg, jpeg. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)],verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='content/',
                    help_text="Accepted formats: png, jpg, jpeg. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)],verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Testimonal(models.Model):
    full_name = models.CharField(max_length=100, unique=True,verbose_name="Full Name")
    testimonal = models.TextField(verbose_name="Testimonal")
    company_name = models.CharField(max_length=100,null=True,blank=True,verbose_name="Company Name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Partner(models.Model):
    company_name = models.CharField(max_length=100, unique=True,verbose_name="Company Name")
    url = models.URLField(max_length=100,null=True,blank=True,verbose_name="Website Link")
    logo = models.ImageField(upload_to='content/',
                    help_text="Accepted formats: png, jpg, jpeg. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)],verbose_name="Logo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name
