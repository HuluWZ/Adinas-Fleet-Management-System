from django import forms
from .models import Slider, About , Service , Testimonal , Partner , Message

class MessageForm(forms.ModelForm):
    class Meta:
        model= Message
        fields =['name','email','phone_number','note']
        widgets ={
            'name': forms.TextInput(attrs={"placeholder": "Your Name / የእርስዎ ስም",'onkeyup':'validateAgain("id_name","name_error")' },),
            'email': forms.TextInput(attrs={"placeholder": "Your Email / የእርስዎ ኢ-ሜይል"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Your Mobile / የእርስዎ ሞባይል", 'class':'form-control', "data-mask": "+251-99999-9999"},),
            'note': forms.Textarea(attrs={'rows': 2,"placeholder":"Special Note / የእርስዎ መልዕክት"}),  
        }
        
class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "Title", },),
            'description': forms.Textarea(attrs={'rows': 3,"placeholder":"Description"}),  # Adjust the rows as needed
            'image':forms.FileInput(attrs={'class':"form-control"}),
        }

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "Title", },),
            'description': forms.Textarea(attrs={'rows': 3,"placeholder":"Description"}),  # Adjust the rows as needed
            'image':forms.FileInput(attrs={'class':"form-control"}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "Title", },),
            'description': forms.Textarea(attrs={'rows': 3,"placeholder":"Description"}),  # Adjust the rows as needed
            'image':forms.FileInput(attrs={'class':"form-control"}),

        }


class TestimonalForm(forms.ModelForm):
    class Meta:
        model = Testimonal
        fields = ['full_name', 'testimonal', 'company_name']
        widgets = {
            'full_name': forms.TextInput(attrs={"placeholder": "Full Name", },),
            'company_name': forms.TextInput(attrs={"placeholder": "Company Name", },),
            'testimonal': forms.Textarea(attrs={'rows': 3,"placeholder":"Testimonial"}),  # Adjust the rows as needed

        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['company_name', 'url', 'logo']
        widgets = {
            'url': forms.TextInput(attrs={"placeholder": "Website Link", },),
            'company_name': forms.TextInput(attrs={"placeholder": "Company Name", },),
            'logo':forms.FileInput(attrs={'class':"form-control"}),
        }
