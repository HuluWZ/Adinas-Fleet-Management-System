import pyotp

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission, Group
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator,RegexValidator

from django_countries.fields import CountryField

allowed_image_extensions = ['png','jpg','jpeg','webp',]
allowed_file_extensions = ['pdf','docx','jpg',]

PHONE_NUMBER_REGEX = RegexValidator(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'Only valid Phone Number is required')
FULL_NAME_REGEX = RegexValidator(r'[A-Za-z]{2,25}[A-Za-z]{2,25}',"Enter a valid text. This value may contain only letters, numbers, and @/./+/-/_ characters")

class UserAccount(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(verbose_name="Email Address",blank=True)
    phone_number = models.CharField(max_length=20,null=True,
                                    unique=True,
                                    validators=[PHONE_NUMBER_REGEX])
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="useraccount_set",
        related_query_name="user",
    ) 
    gender = models.CharField(choices=(('','Select Gender'),('Male',"Male"),
                                       ('Female','Female')),max_length=50,blank=True)
    address = models.CharField(max_length=100,verbose_name="City",blank=True)
    profile_image = models.ImageField(upload_to="accounts/",blank=True,
                    help_text="Accepted formats: png, jpg, jpeg,webp. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)])
    otp_counter = models.IntegerField(default=0)
    otp_secret = models.CharField(max_length=255,default="")
    is_driver = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_both = models.BooleanField(default=False)
    created_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="user_created_by")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="updated_by_user")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    def __str__(self):
        if self.first_name != "" or self.last_name != "":
            return "{} {}".format(self.first_name,self.last_name)
        else:
            return self.username
    def current_otp(self):
        key = self.otp_secret
        if key != "":
            otp_token = pyotp.TOTP(key)
            return str(otp_token.at(self.otp_counter))
        else:
            return "No OTP"


    class Meta:
        ordering = ("-created_date",)


