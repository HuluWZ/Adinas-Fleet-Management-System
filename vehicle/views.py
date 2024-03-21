from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import (
    VehicleData,
    VehicleType,
    VehicleModel,
    VehicleBrand,
    VehicleColor,
    VehicleImage,
    AreaOfInterest
)
from .forms import (
    VehicleForm,
    TypeForm,
    ModelForm,
    BrandForm,
    ColorForm,
    VehicleImageForm,
    AreaOfInterestForm,
)
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Count , Q
from django.core.serializers import serialize

def get_by_vehicle_type():
    result = VehicleData.objects.exclude(is_expired=True).values('vehicle_type__name').annotate(count=Count('vehicle_type'))
    labels = [item['vehicle_type__name'] for item in result]
    data = [item['count'] for item in result]
    return [labels,data]

def get_by_register():
    result = VehicleData.objects.exclude(is_expired=True).exclude(created_by=None).values('created_by').annotate(
                       driver_count=Count('pk', filter=Q(created_by__is_driver=True)),
                       owner_count=Count('pk', filter=Q(created_by__is_owner=True)),
                       admin_count=Count('pk', filter=Q(created_by__is_driver=False, created_by__is_owner=False))
    )    
    if not result:
        return [0, 0, 0]
    else:
        return [item for sublist in result.values_list('driver_count', 'owner_count', 'admin_count') for item in sublist]

class FilterVehicleView(LoginRequiredMixin,View):
    def get(self, request):
        registered_by = request.GET.get('registered_by')
        vehicle_type_id = request.GET.get('vehicle_type')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        vehicles = VehicleData.objects.filter(is_expired=False)
        
        if registered_by:
            if registered_by == 'admin':
                vehicles = vehicles.filter(created_by__is_superuser=True)
            elif registered_by == 'driver':
                vehicles = vehicles.filter(created_by__is_driver=True)
            elif registered_by == 'owner':
                vehicles = vehicles.filter(created_by__is_owner=True)
        
        if vehicle_type_id:
            vehicles = vehicles.filter(vehicle_type_id=vehicle_type_id)
        
        if start_date and end_date:
            vehicles = vehicles.filter(created_at__date__range=[start_date, end_date])
        elif start_date:
            vehicles = vehicles.filter(created_at__date=start_date)
        elif end_date:
            vehicles = vehicles.filter(created_at__date=end_date)
        
        [type_label,type_data] = get_by_vehicle_type()
        driver_owner_admin_counts = get_by_register()
        selected_type = int(vehicle_type_id) if vehicle_type_id and vehicle_type_id.isdigit() else None
        context = {
            'vehicle_data': vehicles,
            'vehicle_type': VehicleType.objects.all(),
            'selected_type': selected_type,
            'selected_user_type': registered_by,
            'start_date': start_date_str,
            'end_date':end_date_str,
            'type_data':type_data,
            'type_label':type_label,
            "driver_owner_admin_counts":driver_owner_admin_counts,
            'register_data'
            'report':'active',
            'report_submenu':'active',
            'subtitle':"Vehicle  Filter List",
        }
        return render(request,"admin/report/vehicle_list.html",context=context)


class CreateInterestView(LoginRequiredMixin, View):
    def get(self, request):
        form = AreaOfInterestForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Add Area Of Interest",
            "page_title": "Add Area Of Interest Form",
            "form": form,
        }
        return render(request, "admin/driver/interest/interest_form.html", context=context)

    def post(self, request):
        form = AreaOfInterestForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Area Of Interest Added successfully")
            return redirect("admin:get_all_interest")
        else:
            context = {
                "form": form,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Area Of Interest Update",
            }
            return render(
                request, "admin/driver/interest/interest_form.html", context=context
            )


class UpdateInterestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(AreaOfInterest, id=vehicle_id)
        form = AreaOfInterestForm(instance=client)  # Create an instance of your form
        context = {
            "object": client,
            "form": form,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Area Of Interest Update",
        }
        return render(request, "admin/driver/interest/interest_detail.html", context=context)

    def post(self, request, vehicle_id):
        client = get_object_or_404(AreaOfInterest, id=vehicle_id)
        form = AreaOfInterestForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Area Of Interest Updated successfully")
            return redirect("admin:get_all_interest")
        else:
            context = {
                "form": form,
                "object": client,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Area Of Interest Update",
            }
            return render(
                request, "admin/driver/interest/interest_detail.html", context=context
            )


class GetAllInterestView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = AreaOfInterest.objects.all()
        context = {
            "vehicle_data": vehicles,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Area Of Interest List",
        }
        return render(request, "admin/driver/interest/interest_list.html", context=context)


class DeleteInterestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(AreaOfInterest, id=vehicle_id)
        client.delete()
        messages.success(request, "Area Of Interest Deleted successfully")
        return redirect("admin:get_all_interest")


class ActivateDeactivateInterestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(AreaOfInterest, id=vehicle_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Area Of Interest  {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_interest")


class UpdateVehicleImageView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        images = VehicleImage.objects.filter(vehicle=vehicle).order_by("-created_at").all()
        form = VehicleImageForm()  
        context = {
            "form": form,
            "object": vehicle,
            "images": images,
            "drivers": "active",
            "drivers_submenu": "active",
            "subtitle": "Vehicle Update",
        }
        return render(request, "admin/vehicle/vehicle_detail.html", context=context)

class RemoveVehicleImage(LoginRequiredMixin, View):
    
    def get(self,request,image_id):
        image = get_object_or_404(VehicleImage, id=image_id)
        image.delete()
        messages.success(request, "Vehicle Image Deleted successfully")
        return redirect("admin:get_all_vehicles")

        
@login_required
def create_vehicle_from_view(request):
    if request.method == 'GET':
        form = VehicleForm()
        context = {"form": form}
        return render(request, "website/vehicle_form.html", context=context)

    elif request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.account = request.user
            vehicle.save()

            images = request.FILES.getlist("vehicle_images")
            for image in images:
                VehicleImage.objects.create(vehicle=vehicle, image=image)

            messages.success(request, "Vehicle Registered successfully")
            return redirect('website:index')  # Replace 'website:index' with the actual URL name for your index page

        else:
            context = {"form": form}
            return render(request, "website/vehicle_form.html", context=context)

class CreateColorView(LoginRequiredMixin, View):
    def get(self, request):
        form = ColorForm()
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Add Vehicle Color",
            "page_title": "Add Vehicle Color Form",
            "form": form,
        }
        return render(request, "admin/driver/color/color_form.html", context=context)

    def post(self, request):
        form = ColorForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Color Added successfully")
            return redirect("admin:get_all_color")
        else:
            context = {
                "form": form,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Color ",
            }
            return render(
                request, "admin/driver/color/color_form.html", context=context
            )


class UpdateColorView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleColor, id=vehicle_id)
        form = ColorForm(instance=client)  # Create an instance of your form
        context = {
            "object": client,
            "form": form,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Color Update",
        }
        return render(request, "admin/driver/color/color_detail.html", context=context)

    def post(self, request, vehicle_id):
        client = get_object_or_404(VehicleColor, id=vehicle_id)
        form = ColorForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Color Updated successfully")
            return redirect("admin:get_all_color")
        else:
            context = {
                "form": form,
                "object": client,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Color Update",
            }
            return render(
                request, "admin/driver/color/color_detail.html", context=context
            )


class GetAllColorView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = VehicleColor.objects.all()
        context = {
            "vehicle_data": vehicles,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Color List",
        }
        return render(request, "admin/driver/color/color_list.html", context=context)


class DeleteColorView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleColor, id=vehicle_id)
        client.delete()
        messages.success(request, "Vehicle Color Deleted successfully")
        return redirect("admin:get_all_color")


class ActivateDeactivateColorView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleColor, id=vehicle_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Vehicle Color {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_color")


class GetOneColorView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleColor, id=vehicle_id)
        form = ColorForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Color Detail",
            "page_title": "Update Vehicle Color Detail",
            "object": client,
            "form": form,
        }
        return render(request, "admin/driver/color/color_detail.html", context=context)


class CreateBrandView(LoginRequiredMixin, View):
    def get(self, request):
        form = BrandForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Add Vehicle Brand",
            "page_title": "Add Vehicle Brand Form",
            "form": form,
        }
        return render(request, "admin/driver/brand/brand_form.html", context=context)

    def post(self, request):
        form = BrandForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Brand Added successfully")
            return redirect("admin:get_all_brand")
        else:
            context = {
                "form": form,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Brand Update",
            }
            return render(
                request, "admin/driver/brand/brand_form.html", context=context
            )


class UpdateBrandView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleBrand, id=vehicle_id)
        form = BrandForm(instance=client)  # Create an instance of your form
        context = {
            "object": client,
            "form": form,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Brand Update",
        }
        return render(request, "admin/driver/brand/brand_detail.html", context=context)

    def post(self, request, vehicle_id):
        client = get_object_or_404(VehicleBrand, id=vehicle_id)
        form = BrandForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Brand Updated successfully")
            return redirect("admin:get_all_brand")
        else:
            context = {
                "form": form,
                "object": client,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Brand Update",
            }
            return render(
                request, "admin/driver/brand/brand_detail.html", context=context
            )


class GetAllBrandView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = VehicleBrand.objects.all()
        context = {
            "vehicle_data": vehicles,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Brand List",
        }
        return render(request, "admin/driver/brand/brand_list.html", context=context)


class DeleteBrandView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleBrand, id=vehicle_id)
        client.delete()
        messages.success(request, "Vehicle Brand Deleted successfully")
        return redirect("admin:get_all_brand")


class ActivateDeactivateBrandView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleBrand, id=vehicle_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Vehicle Brand {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_brand")


class GetOneBrandView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleBrand, id=vehicle_id)
        form = BrandForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Brand Detail",
            "page_title": "Update Vehicle Brand Detail",
            "object": client,
            "form": form,
        }
        return render(request, "admin/driver/brand/brand_detail.html", context=context)


class CreateModelView(LoginRequiredMixin, View):
    def get(self, request):
        form = ModelForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Add Vehicle Model",
            "page_title": "Add Vehicle Model Form",
            "form": form,
        }
        return render(request, "admin/driver/model/model_form.html", context=context)

    def post(self, request):
        form = ModelForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Model Added successfully")
            return redirect("admin:get_all_model")
        else:
            context = {
                "form": form,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Model Update",
            }
            return render(
                request, "admin/driver/model/model_form.html", context=context
            )


class UpdateModelView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleModel, id=vehicle_id)
        form = ModelForm(instance=client)  # Create an instance of your form
        context = {
            "object": client,
            "form": form,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Model Update",
        }
        return render(request, "admin/driver/model/model_detail.html", context=context)

    def post(self, request, vehicle_id):
        client = get_object_or_404(VehicleModel, id=vehicle_id)
        form = ModelForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Model Updated successfully")
            return redirect("admin:get_all_model")
        else:
            context = {
                "form": form,
                "object": client,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Model Update",
            }
            return render(
                request, "admin/driver/model/model_detail.html", context=context
            )


class GetAllModelView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = VehicleModel.objects.all()
        context = {
            "vehicle_data": vehicles,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Model List",
        }
        return render(request, "admin/driver/model/model_list.html", context=context)


class DeleteModelView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleModel, id=vehicle_id)
        client.delete()
        messages.success(request, "Vehicle Model Deleted successfully")
        return redirect("admin:get_all_model")


class ActivateDeactivateModelView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleModel, id=vehicle_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Vehicle Model {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_model")


class GetOneModelView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleModel, id=vehicle_id)
        form = ModelForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Model Detail",
            "page_title": "Update Vehicle Model Detail",
            "object": client,
            "form": form,
        }
        return render(request, "admin/driver/model/model_detail.html", context=context)


class CreateTypeView(LoginRequiredMixin, View):
    def get(self, request):
        form = TypeForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Add Vehicle Type",
            "page_title": "Add Vehicle Type Form",
            "form": form,
        }
        return render(request, "admin/driver/type/type_form.html", context=context)

    def post(self, request):
        form = TypeForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Type Added successfully")
            return redirect("admin:get_all_type")
        else:
            context = {
                "form": form,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle Type Update",
            }
            return render(
                request, "admin/driver/type/type_form.html", context=context
            )


class UpdateTypeView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleType, id=vehicle_id)
        form = TypeForm(instance=client)  # Create an instance of your form
        context = {
            "object": client,
            "form": form,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Type Update",
        }
        return render(request, "admin/driver/type/type_detail.html", context=context)

    def post(self, request, vehicle_id):
        client = get_object_or_404(VehicleType, id=vehicle_id)
        form = TypeForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Vehicle Type Updated successfully")
            return redirect("admin:get_all_type")
        else:
            context = {
                "form": form,
                "object": client,
                "settings": "active",
                "settings_submenu": "active",
                "subtitle": "Vehicle  Type Update",
            }
            return render(
                request, "admin/driver/type/type_detail.html", context=context
            )


class GetAllTypeView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = VehicleType.objects.all()
        context = {
            "vehicle_data": vehicles,
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Type List",
        }
        return render(request, "admin/driver/type/type_list.html", context=context)


class DeleteTypeView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleType, id=vehicle_id)
        client.delete()
        messages.success(request, "Vehicle Type Deleted successfully")
        return redirect("admin:get_all_type")


class ActivateDeactivateTypeView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleType, id=vehicle_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Vehicle Type {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_type")


class GetOneTypeView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleType, id=vehicle_id)
        form = TypeForm()  # Create an instance of your form
        context = {
            "settings": "active",
            "settings_submenu": "active",
            "subtitle": "Vehicle Type Detail",
            "page_title": "Update Vehicle Type Detail",
            "object": client,
            "form": form,
        }
        return render(request, "admin/driver/type/type_detail.html", context=context)


class CreateVehicleView(LoginRequiredMixin, View):
    def get(self, request):
        form = VehicleForm()  # Create an instance of your form
        context = {
            "drivers": "active",
            "drivers_submenu": "active",
            "subtitle": "Add Vehicle",
            "page_title": "Add Vehicle Form",
            "form": form,
        }
        return render(request, "admin/vehicle/vehicle_form.html", context=context)

    def post(self, request):
        form = VehicleForm(request.POST, request.FILES)
        
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.created_by = request.user
            selected_areas_of_interest = form.cleaned_data['area_of_interests'].values_list('id', flat=True)
            vehicle.save()
            for selected_area in selected_areas_of_interest:  
              vehicle.area_of_interests.add(selected_area)
            images = request.FILES.getlist("vehicle_images")
            for image in images:
                print(f"Looped Vehicle Image..............{image}")
                VehicleImage.objects.create(vehicle=vehicle, image=image)

            messages.success(request, "Vehicle Created successfully")
            return redirect("admin:get_all_vehicles")
        else:
            context = {
                "form": form,
                "drivers": "active",
                "drivers_submenu": "active",
                "subtitle": "Vehicle Create",
            }
            return render(request, "admin/vehicle/vehicle_form.html", context=context)


class UpdateVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        images = VehicleImage.objects.filter(vehicle=vehicle).order_by('-created_at').all()
        has_images = images.exists()
        form = VehicleForm(instance=vehicle)
        form2 = VehicleImageForm()  
        context = {
            "form": form,
            "form2":form2,
            "object": vehicle,
            "images": images,
            "drivers": "active",
            "has_images": has_images,
            "drivers_submenu": "active",
            "subtitle": "Vehicle Update",
        }
        return render(request, "admin/vehicle/vehicle_detail.html", context=context)

    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        images = VehicleImage.objects.filter(vehicle=vehicle)
        has_images = images.exists()
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        form2 = VehicleImageForm()
        if 'submit_form1' in request.POST:
          if form.is_valid():
            form.save()
            messages.success(request, "Vehicle Updated successfully")
            return redirect("admin:get_all_vehicles")
          else:
            context = {
                "form": form,
                "form2": form2,
                "images": images,
                "has_images": has_images,
                "object": vehicle,
                "drivers": "active",
                "drivers_submenu": "active",
                "subtitle": "Vehicle Update",
            }
            return render(request, "admin/vehicle/vehicle_detail.html", context=context)
        if 'submit_form2' in request.POST:
           form = VehicleImageForm(request.POST,request.FILES)
           uploaded_images = request.FILES.getlist("image")
           if uploaded_images:
             uploaded_images = request.FILES.getlist("image")
             for image in uploaded_images:
                new_vehicle_image = VehicleImage(vehicle=vehicle, image=image)
                new_vehicle_image.save()
             messages.success(request, f" {len(uploaded_images)} Vehicle Image Uploaded successfully")
            # return redirect("admin:get_all_vehicles")
             return redirect('admin:update_vehicle', vehicle_id=vehicle_id)
        else:
            context = {
                "form": form,
                "images": images,
                "has_images": has_images,
                "object": vehicle,
                "drivers": "active",
                "drivers_submenu": "active",
                "subtitle": "Vehicle Update",
            }
            return render(request, "admin/vehicle/vehicle_detail.html", context=context)


class GetAllVehiclesView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = VehicleData.objects.filter(is_expired=False)
        context = {
            "vehicle_data": vehicles,
            "drivers": "active",
            "drivers_submenu": "active",
            "subtitle": "Vehicle List",
        }
        return render(request, "admin/vehicle/vehicle_list.html", context=context)

class GetAllExpiredVehicleView(LoginRequiredMixin,View):
    def get(self, request):
        drives = VehicleData.objects.filter(is_expired=True)
        context = {
            'vehicle_data': drives ,
            'archive':'active',
            'archive_submenu':'active',
            'subtitle':"Expired Vehicles List",
        }
        return render(request,"admin/recycle/vehicle_list.html",context=context)


class GetOneVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleData, id=vehicle_id)
        form = VehicleForm()  # Create an instance of your form
        context = {
            "drivers": "active",
            "drivers_submenu": "active",
            "subtitle": "Vehicle Detail",
            "page_title": "Update Vehicle Detail",
            "object": client,
            "form": form,
        }
        return render(request, "admin/vehicle/vehicle_detail.html", context=context)


class DeleteVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        vehicle.delete()
        messages.success(request, "Vehicle Deleted successfully")
        return redirect("admin:get_all_vehicles")


class ExpireVehicleView(LoginRequiredMixin,View):
    def get(self, request, vehicle_id):
        drive = get_object_or_404(VehicleData, id=vehicle_id)
        drive.is_expired = not drive.is_expired
        drive.save()
        message = f'Vehicle {"Removed" if drive.is_expired else "Restored"} successfully'
        url = "admin:recycle_all_vehicles" if not drive.is_expired else "admin:get_all_vehicles"
        messages.success(request, message)
        return redirect(url)

class ActivateDeactivateVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleData, id=vehicle_id)
        client.is_active = not client.is_active
        client.save()
        message = (
            f'Vehicle {"Activated" if client.is_active else "Deactivated"} successfully'
        )
        messages.success(request, message)
        return redirect("admin:get_all_vehicles")
