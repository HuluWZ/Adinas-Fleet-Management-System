from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name','company_email','company_phone','address', 'license', 'focal_person_name', 'phone_number','email']
        widgets = {
            'company_name': forms.TextInput(attrs={"placeholder": "Company Name", },),
            'company_email': forms.TextInput(attrs={"placeholder": "Company Email", },),
            'company_phone': forms.TextInput(attrs={"placeholder": "Company Phone","data-mask": "+251-11111-1111" },),
            'address': forms.TextInput(attrs={"placeholder": "Address", },),
            'license':forms.FileInput(attrs={'class':"form-control"}),
            'focal_person_name': forms.TextInput(attrs={"placeholder": "Focal Person Name", },),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number","data-mask": "+251-99999-9999" },),
            'email': forms.TextInput(attrs={"placeholder": "Email", },),
        }

