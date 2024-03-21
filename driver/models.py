from django.db import models
from django.core.validators import RegexValidator,FileExtensionValidator
from accounts.models import UserAccount
 
allowed_image_extensions = ['png','jpg','jpeg']
allowed_file_extensions = ['png','jpg','jpeg','pdf']

PHONE_NUMBER_REGEX = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Only valid Phone Number is required')

class Owner(models.Model):
    account = models.OneToOneField(UserAccount,on_delete=models.CASCADE,null=True,blank=True,related_name="owner")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserAccount,on_delete=models.RESTRICT,null=True,blank=True,related_name="owner_created_by")
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="updated_by_user")
    last_updated_date = models.DateTimeField(null=True)
    is_expired = models.BooleanField(default=False)
       
    class Meta:
        ordering = ['-created_at']


class Driver(models.Model):
    account = models.OneToOneField(UserAccount,on_delete=models.CASCADE,null=True,blank=True,related_name="driver")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserAccount,on_delete=models.RESTRICT,null=True,blank=True,related_name="driver_created_by")
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="updated_by_user")
    last_updated_date = models.DateTimeField(null=True)
    is_available = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_at']

      
