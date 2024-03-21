from django import forms

from .models import (
    VehicleBooking,
    VehicleType,
    VehicleBrand,
    VehicleModel,
    AssignedVehicle,
)
from vehicle.models import VehicleData
from client.models import Client


class AssignedVehicleForm(forms.ModelForm):
    class Meta:
        model = AssignedVehicle
        fields = ["vehicle_request", "vehicle"]
        required_fields = ["vehicle"]

    def __init__(self, *args, **kwargs):
        vehicles = kwargs.pop("vehicles", None)
        super().__init__(*args, **kwargs)
        self.fields["vehicle_request"].required = False
        self.fields["vehicle"].required = True
        # if vehicles:
        self.update_vehicle_choices(vehicles)
        # else:
            # self.update_vehicle_choices(VehicleData.objects.filter(is_available=True,is_expired=False))

    def get_vehicle_display(self, vehicle):
        return f"{vehicle.plate_number}  {vehicle.vehicle_type} @ {vehicle.production_year}"

    def update_vehicle_choices(self, vehicles):
        choices = [
            (vehicle.pk, self.get_vehicle_display(vehicle)) for vehicle in vehicles
        ]
        self.fields["vehicle"].choices = choices


class VehicleBookingForm(forms.ModelForm):
    client_info = forms.ModelChoiceField(
        queryset=Client.objects.filter(is_active=True),
        label="Client",
        empty_label="Select Client Info",
    )  # Adds a placeholder at the top of the dropdown)
    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.filter(is_active=True),
        required=True,
        label="Vehicle Type",
        empty_label="Select Vehicle Type",
    )
    model = forms.ModelChoiceField(
        queryset=VehicleModel.objects.filter(is_active=True),
        required=False,
        label="Model",
        empty_label="Select Model",
    )
    brand = forms.ModelChoiceField(
        queryset=VehicleBrand.objects.filter(is_active=True),
        required=False,
        label="Make",
        empty_label="Select Make",
    ) 

    class Meta:
        model = VehicleBooking
        fields = [
            "client_info",
            "pickup",
            "drop_off",
            "daily_price",
            "no_of_vehicles",
            "vehicle_type",
            "brand",
            "model",
            "production_year",
            "start_date",
            "end_date",
            "remark",
        ]
        widgets = {
            "pickup": forms.TextInput(
                attrs={"placeholder": "Pick Up"},
            ),
            "drop_off": forms.TextInput(
                attrs={"placeholder": "Drop Off"},
            ),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "production_year":forms.NumberInput(attrs={"placeholder": "Production Year"}),
            "remark":forms.TextInput(attrs={"placeholder": "Enter Remarks if Any"})
        }
