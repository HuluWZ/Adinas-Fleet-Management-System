from django import forms
from .models import Owner, Driver
from accounts.models import UserAccount
class DriverForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('driver', 'Is Driver'),
        ('owner', 'Is Owner'),
        ('both', 'Is Both'),
    )

    role = forms.ChoiceField(label='Role', widget=forms.RadioSelect, choices=ROLE_CHOICES)


    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name','gender','profile_image',
                    'address','username',
                    'email', 'phone_number',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name",'onkeyup':'validateAgain("id_first_name","fname_error")' },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name",'onkeyup':'validateAgain("id_last_name","lname_error")'},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
            'address':forms.TextInput(attrs={'placeholder':"City",'onkeyup':'validateAgain("id_address","had_error")'}),
            'profile_image':forms.FileInput(attrs={'class':"form-control"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if not role:
            raise forms.ValidationError("Please select a role.")

        return cleaned_data
class OwnerForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('driver', 'Is Driver'),
        ('owner', 'Is Owner'),
        ('both', 'Is Both'),
    )

    role = forms.ChoiceField(label='Role', widget=forms.RadioSelect, choices=ROLE_CHOICES)
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name','gender','profile_image',
                    'address','username',
                    'email', 'phone_number',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name",'onkeyup':'validateAgain("id_first_name","fname_error")' },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name",'onkeyup':'validateAgain("id_last_name","lname_error")'},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
            'address':forms.TextInput(attrs={'placeholder':"City",'onkeyup':'validateAgain("id_address","had_error")'}),
            'profile_image':forms.FileInput(attrs={'class':"form-control"}),
        }
