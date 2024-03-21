from django import forms
from django.db.models import Q , Count
from django.core.validators import FileExtensionValidator
from accounts.models import UserAccount
from .models import (
    VehicleData,
    VehicleType,
    VehicleBrand,
    VehicleModel,
    VehicleColor,
    VehicleImage,
    AreaOfInterest
)


allowed_image_extensions = ["png", "jpg", "jpeg"]

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    help_text = ("Accepted formats: png, jpg, jpeg. Max file size 10 MB",)

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(
                attrs={"class": "form-control"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class VehicleImageForm(forms.ModelForm):        
    class Meta:
        model = VehicleImage
        fields = ("image",)
        widgets = {
            "image": forms.TextInput(
                attrs={"class": "multiple-files-filepond","type":"file", "multiple": True}
            )
        }

class VehicleWebForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleWebForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['area_of_interests'].required = False
            self.fields['vehicle_images'].required = False

    area_of_interests = forms.ModelMultipleChoiceField(
        queryset=AreaOfInterest.objects.filter(is_active=True),
        label="Area Of Interest",
    )

    color = forms.ModelChoiceField(
        queryset=VehicleColor.objects.filter(is_active=True),
        label="Color",
        empty_label="Select Color",
    )
    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.filter(is_active=True),
        label="Vehicle Type",
        empty_label="Select Vehicle Type",
    )
    model = forms.ModelChoiceField(
        queryset=VehicleModel.objects.filter(is_active=True),
        label="Model",
        empty_label="Select Model",
    )
    brand = forms.ModelChoiceField(
        queryset=VehicleBrand.objects.filter(is_active=True),
        label="Make",
        empty_label="Select Make",
    )

    production_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Production Year"})
    )
    vehicle_images = MultipleFileField(label="Upload Vehicle Images")

    class Meta:
        model = VehicleData
        fields = [
            "plate_number",
            "area_of_interests",
            "color",
            "transmission",
            "fuel_type",
            "driver_status",
            "address",
            "price_per_day",
            "vehicle_type",
            "libre",
            "license",
            "brand",
            "model",
            "production_year",
        ]
        widgets = {
            "plate_number": forms.TextInput(
                attrs={"placeholder": "Plate Number"},
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "City"},
            ),
            "libre": forms.FileInput(attrs={"class": "form-control"}),
            "libre": forms.FileInput(attrs={"class": "form-control"}),
            "license": forms.FileInput(attrs={"class": "form-control"}),
            "area_of_interests":   forms.SelectMultiple,  
        }
        
    def clean_vehicle_images(self):
        data = self.cleaned_data['vehicle_images']
        instance = self.instance  
        print(" Instance ",instance,instance.pk, data)
        if not instance.pk and not data:
            raise forms.ValidationError("Images are required when creating a new vehicle.")
        
        return data

class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['area_of_interests'].required = False

    area_of_interests = forms.ModelMultipleChoiceField(
        queryset=AreaOfInterest.objects.filter(is_active=True),
        label="Area Of Interest",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    color = forms.ModelChoiceField(
        queryset=VehicleColor.objects.filter(is_active=True),
        label="Color",
        empty_label="Select Color",
        # widget=forms.Select(attrs={'class':'choices form-select'})
    )
    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.filter(is_active=True),
        label="Vehicle Type",
        empty_label="Select Vehicle Type",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    model = forms.ModelChoiceField(
        queryset=VehicleModel.objects.filter(is_active=True),
        label="Model",
        empty_label="Select Model",
        # widget=forms.Select(attrs={'class': 'choices form-select'})
    )
    brand = forms.ModelChoiceField(
        queryset=VehicleBrand.objects.filter(is_active=True),
        label="Make",
        empty_label="Select Make",
        # widget=forms.Select(attrs={'class':'choices form-select'})
    )

    account = forms.ModelChoiceField(
        queryset=UserAccount.objects.annotate(vehicle_count=Count('vehicle')).filter(
            Q(is_driver=True, vehicle_count=0) |
            Q(is_owner=True) |
            Q(is_both=True)
        ),
        label="Owner/Driver",
        empty_label="Select Owner/Driver",
        # widget=forms.Select(attrs={'class': 'choices form-select'})
    )

    production_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Production Year"})
    )
    vehicle_images = MultipleFileField(label="Upload Vehicle Images",required=False)

    class Meta:
        model = VehicleData
        fields = [
            "account",
            "plate_number",
            "area_of_interests",
            "color",
            "transmission",
            "fuel_type",
            "driver_status",
            "address",
            "price_per_day",
            "vehicle_type",
            "libre",
            "license",
            "brand",
            "model",
            "production_year",
        ]
        widgets = {
            "plate_number": forms.TextInput(
                attrs={"placeholder": "Plate Number"},
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "City"},
            ),
            "libre": forms.FileInput(attrs={"class": "form-control"}),
            "libre": forms.FileInput(attrs={"class": "form-control"}),
            "license": forms.FileInput(attrs={"class": "form-control"}),
            }
        
    def clean_vehicle_images(self):
        data = self.cleaned_data['vehicle_images']
        instance = self.instance  # The instance being updated
        print(" Instance ",instance,instance.pk, data)
        if not instance.pk and not data:
            raise forms.ValidationError("Images are required when creating a new vehicle.")
        
        return data


class AreaOfInterestForm(forms.ModelForm):
    class Meta:
        model = AreaOfInterest
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Area Of Interest",
                },
            ),
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Vehicle Type",
                },
            ),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = VehicleBrand
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Vehicle Brand",
                },
            ),
        }


class ModelForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Vehicle Model",
                },
            ),
        }


class ColorForm(forms.ModelForm):
    class Meta:
        model = VehicleColor
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Vehicle Color",
                },
            ),
        }
