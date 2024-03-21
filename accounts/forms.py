from django import forms 
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext as _
from django.contrib.admin.forms import AdminAuthenticationForm ,AuthenticationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.models import fields
import pyotp
from accounts.models import  UserAccount 
from django.contrib.auth import login , authenticate
import datetime
from django.utils import timezone

class UserSignupWebForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('driver', 'I am the Driver / አሽከርካሪ'),
        ('owner', 'I am the Owner/ ባለቤት'),
        ('both', 'I am Both the Owner and the Driver/ ሁለቱም ነኝ'),
    )

    role = forms.ChoiceField(label='Which type of user are you ?/ የርስዎ ሃላፊነት ምንድነው ? ', widget=forms.RadioSelect, choices=ROLE_CHOICES)


    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name','address', 'phone_number',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name/ስም",'onkeyup':'validateAgain("id_first_name","fname_error")' },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name/የአባት ስም",'onkeyup':'validateAgain("id_last_name","lname_error")'},),
            'address': forms.TextInput(attrs={"placeholder": "City / አድራሻ(ከተማ)"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number/ስልክ ቁጥር ", "data-mask": "+251-99999-9999"},),
        }
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if not role:
            raise forms.ValidationError("Please select a role.")

        return cleaned_data
    
class YearSelectionForm(forms.Form):
    year = forms.IntegerField(label='Select Year', widget=forms.Select(choices=[]))
    
    def __init__(self, *args, **kwargs):
        super(YearSelectionForm, self).__init__(*args, **kwargs)
        self.fields['year'].choices = [(year, year) for year in range(2020, timezone.now().year + 1)]
        self.fields['year'].initial = timezone.now().year
        
class CustomAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(
        max_length=6,
        label="OTP",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the OTP',
                                      'class':'form-control'})
    )
    class Meta:
        fields = [ 'otp']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields.pop('password', None)

    def clean(self):
        cleaned_data = super().clean()
        user_otp = cleaned_data.get('otp')
        phone_number = self.request.session.get('phone_number')
        print(" Phone Number and OTP ",phone_number,user_otp)
        if phone_number and user_otp:
            user = UserAccount.objects.filter(phone_number=phone_number).first()            
            print(" User ",user)
            if not user:
                print(" User not found")
                raise ValidationError("User not found")
            
            print(" User Token Verify")
            otp_secret = user.otp_secret
            otp = pyotp.TOTP(otp_secret, interval=2000)
            print(" OTP ",user_otp,user)
            print(" Verify ",otp.verify(user_otp))

            if not otp.verify(user_otp):
                raise ValidationError("Invalid OTP")
            user = authenticate(request=self.request, username=phone_number)
            print(" USER AUTH ",user)
            if user:
                login(self.request, user)
            else:
                raise ValidationError("User authentication failed")


        return cleaned_data
    
class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number/ስልክ ቁጥር ",
        widget= forms.TextInput(attrs={'placeholder': 'Enter your phone number/ስልክ ቁጥር ያስገቡ',
                                       'class':'form-control',
                                       "data-mask": "+251-99999-9999"})
    )
class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        label="OTP",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the OTP/የተላከሎትን የይለፍ ቃል ያስገቡ'})
    )

class AdminLoginForm(AdminAuthenticationForm):
    username = forms.CharField(label=_('Email / Username'),widget=forms.TextInput(
        attrs={'placeholder':'Email / Username','class':'form-control form-control-xl'}
    ))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'current-password',
                            'class':'form-control form-control-xl'
        }),
    )

# Abstract User Sign Up Form where the other forms extend this form.
class AbstractUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Password"},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Re-Type Password"},
    ))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name','gender','profile_image',
                  'username', 'email', 'phone_number','is_superuser')
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class AFMSUserSignUpForm(AbstractUserCreationForm):
    class Meta(AbstractUserCreationForm.Meta):
        fields = ('first_name', 'last_name','gender',
                    'address',
                  'username', 'email', 'phone_number',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name",'onkeyup':'validateAgain("id_first_name","fname_error")' },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name",'onkeyup':'validateAgain("id_last_name","lname_error")'},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
            'address':forms.TextInput(attrs={'placeholder':"City",'onkeyup':'validateAgain("id_address","had_error")'}),
            'profile_image':forms.FileInput(attrs={'class':"form-control"}),
        }
    
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        print(user)
        user.is_active=False
        user.is_staff = True
        user.is_superuser=False
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        return user
        

class AFMSUserCreationForm(AbstractUserCreationForm):
    """
    this form is for industry admins for creating company users.
    """
    
    user_type = forms.ModelMultipleChoiceField(
        label="User Role Group",
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={}),
        required=False
    )
    # designation = forms.CharField(max_length=255, widget=forms.TextInput(
    #     attrs={'class':'form-control','placeholder':'Responsiblity'}
    # ))
    class Meta(AbstractUserCreationForm.Meta):
        fields = ('first_name', 'last_name','gender','address'
                    ,'profile_image',
                  'username', 'email', 'phone_number','is_superuser')
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
            'address':forms.TextInput(attrs={'placeholder':"Address"}),
            'profile_image':forms.FileInput(attrs={'class':"form-control"}),
        }
    
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        # user.is_staff = True
        user.is_superuser=False
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        user.groups.set(self.cleaned_data.get("user_type"))
        return user

class AFMSUserUpdateForm(forms.ModelForm):
    """
    this form is for industry admins for creating company users.
    """
    class Meta:
        model=UserAccount
        fields = ('first_name', 'last_name','username', 'email', 'phone_number','groups',
                'gender','address',
                'profile_image','is_superuser')
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
            'address':forms.TextInput(attrs={'placeholder':"City"}),
            'profile_image':forms.FileInput(attrs={'class':"form-control"}),
        }

class AFMSUserProfileForm(forms.ModelForm):
    """
    """
    class Meta:
        model=UserAccount
        fields = ('first_name', 'last_name','username', 'email', 'phone_number',
                'gender','address',
                'profile_image',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
            'address':forms.TextInput(attrs={'placeholder':"City"}),
            'profile_image':forms.FileInput(attrs={'class':"form-control"}),
        }



class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('__all__')
        widgets = {
            'permissions': forms.Select(attrs={'class': 'form-control listbox', 'multiple': "multiple"})
        }

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group

class UserPasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error('password2', error)
                
 