from datetime import datetime
import json

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.db.models import Count, Q
from booking.forms import AssignedVehicleForm, VehicleBookingForm
from booking.models import AssignedVehicle, VehicleBooking, Notification as NotificaionModel
from utils.telegram import send_telegram_message
from client.models import Client
from vehicle.models import VehicleData, VehicleType
from utils.sms_messages import sms_api_router
from django.contrib.sites.shortcuts import get_current_site
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message


# Create your views here.
def get_by_vehicle_type():
    result = (
        VehicleBooking.objects.exclude(is_expired=True)
        .values("vehicle_type__name")
        .annotate(count=Count("vehicle_type"))
    )
    labels = [item["vehicle_type__name"] for item in result]
    data = [item["count"] for item in result]
    return [labels, data]


def get_by_client():
    result = (
        VehicleBooking.objects.exclude(is_expired=True)
        .values("client_info__company_name")
        .annotate(count=Count("client_info"))
    )
    labels = [item["client_info__company_name"] for item in result]
    data = [item["count"] for item in result]
    return [labels, data]


class FilterVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request):
        client_id = request.GET.get("client")
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")
        vehicle_type_id = request.GET.get("vehicle_type")

        start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d").date()
            if start_date_str
            else None
        )
        end_date = (
            datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        )

        vehicle_requests = VehicleBooking.objects.all()

        if client_id:
            vehicle_requests = vehicle_requests.filter(client_info_id=client_id)
        if start_date:
            vehicle_requests = vehicle_requests.filter(start_date__gte=start_date)
        if end_date:
            vehicle_requests = vehicle_requests.filter(end_date__lte=end_date)
        if vehicle_type_id:
            vehicle_requests = vehicle_requests.filter(vehicle_type_id=vehicle_type_id)

        [type_label, type_data] = get_by_vehicle_type()
        [labels, data] = get_by_client()
        selected_type = (
            int(vehicle_type_id)
            if vehicle_type_id and vehicle_type_id.isdigit()
            else None
        )
        # selected_client = int(client_id) if client_id is not None else None
        selected_client = int(client_id) if client_id and client_id.isdigit() else None

        print(" client_type_counts ", type_data[0], type_label)

        context = {
            "vehicle_data": vehicle_requests,
            "selected_client": selected_client,
            "selected_type": selected_type,
            "vehicle_type": VehicleType.objects.all(),
            "clients": Client.objects.filter(is_expired=False),
            "start_date": start_date_str,
            "type_data": type_data,
            "type_label": type_label,
            "label_counts": labels,
            "data_counts": data,
            "end_date": end_date_str,
            "report": "active",
            "report_submenu": "active",
            "subtitle": "Vehicle Booking Filter List",
        }
        return render(request, "admin/report/booking_list.html", context=context)


class MarkNotificationSeenView(LoginRequiredMixin, View):

    def get(self, request, pk, vehicle_id):
        try:
            notification = get_object_or_404(NotificaionModel, pk=pk)
            notification.is_seen = True
            notification.save()
            booking = get_object_or_404(VehicleBooking, pk=vehicle_id)
            url = reverse("admin:assign_request", kwargs={"vehicle_id": vehicle_id})
            return redirect(url)
        except VehicleBooking.DoesNotExist:
            return redirect("admin:get_all_request")


class CreateVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request):
        form = VehicleBookingForm()  # Create an instance of your form
        context = {
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Add Vehicle Request",
            "page_title": "Add Vehicle Request Form",
            "form": form,
        }
        return render(request, "admin/request/request_form.html", context=context)

    def post(self, request):
        form = VehicleBookingForm(request.POST)
        if form.is_valid():
            drive = form.save()
            messages.success(request, "Vehicle Request Added successfully")
            return redirect("admin:get_all_request")
        else:
            context = {
                "requests": "active",
                "requests_submenu": "active",
                "subtitle": "Add Vehicle Request",
                "page_title": "Add Vehicle Request Form",
                "form": form,
            }
            return render(request, "admin/request/request_form.html", context=context)


class UpdateVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        driver = get_object_or_404(VehicleBooking, id=vehicle_id)
        form = VehicleBookingForm(instance=driver)  # Create an instance of your form
        context = {
            "form": form,
            "object": driver,
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Vehicle Request Update",
        }
        return render(request, "admin/request/request_detail.html", context=context)

    def post(self, request, vehicle_id):
        drive = get_object_or_404(VehicleBooking, id=vehicle_id)
        form = VehicleBookingForm(request.POST, instance=drive)
        if form.is_valid():
            drive = form.save()
            messages.success(request, "Vehicle Request Updated successfully")
            return redirect("admin:get_all_request")
        else:
            context = {
                "form": form,
                "object": drive,
                "requests": "active",
                "requests_submenu": "active",
                "subtitle": "Vehicle Request Update",
            }
            return render(request, "admin/request/request_detail.html", context=context)


class AssignVehicleToVehicleRequestView(LoginRequiredMixin, View):

    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleBooking, id=vehicle_id)
        assigned_vehicle_ids = AssignedVehicle.objects.filter(
            vehicle_request=vehicle_id
        ).values_list("vehicle__id", flat=True)
        vehicles = VehicleData.objects.filter(
            is_available=True, is_expired=False
        ).exclude(id__in=assigned_vehicle_ids)
        assigned = AssignedVehicle.objects.filter(
            vehicle_request=vehicle, is_terminated=False
        )
        if vehicle.brand != None:
            vehicles = vehicles.filter(brand__id=vehicle.brand.id)
        if vehicle.model != None:
            vehicles = vehicles.filter(model__id=vehicle.model.id)
        if vehicle.vehicle_type != None:
            vehicles = vehicles.filter(vehicle_type__id=vehicle.vehicle_type.id)
        # if vehicle.production_year != None:
        #         vehicles = vehicles.filter(production_year__gte=vehicle.production_year)
        form = AssignedVehicleForm(vehicles=vehicles)
        context = {
            "form": form,
            "object": vehicle,
            "vehicles": vehicles,
            "assigned": assigned,
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Assign Vehicle For Current Booking",
        }
        return render(
            request, "admin/request/assign_driver_detail.html", context=context
        )

    def post(self, request, vehicle_id):
        v_id_from_form = request.POST.getlist("vehicle")
        vehicle_request = get_object_or_404(VehicleBooking, id=vehicle_id)
        assigned_vehicle_ids = AssignedVehicle.objects.filter(
            vehicle_request=vehicle_id
        ).values_list("vehicle__id", flat=True)
        vehicle = VehicleData.objects.filter(
            is_available=True, is_expired=True
        ).exclude(id__in=assigned_vehicle_ids)
        # assigned = AssignedVehicle.objects.filter(vehicle_request=vehicle_request,is_terminated=False)
        assigned = AssignedVehicle.objects.filter(
            vehicle_request=vehicle_request, is_terminated=False
        )  # .select_related('vehicle').prefetch_related('vehicle__images')
        # form = AssignedVehicleForm({'vehicle':v_id_from_form,'vehicle_request':vehicle_id})
        form = AssignedVehicleForm(
            request.POST or None,
            vehicles=vehicle,
            initial={"vehicle_request": vehicle_request.id, "vehicle": vehicle},
        )
        context = {
            "form": form,
            "object": vehicle_request,
            "vehicles": vehicle,
            "assigned": assigned,
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Vehicle Assign Update",
        }
        if form.is_valid():
            selected_vehicle_ids = form.cleaned_data["vehicle"]
            selected_vehicles = VehicleData.objects.filter(id__in=v_id_from_form)
            for vehicle in selected_vehicles:
                AssignedVehicle.objects.create(
                    vehicle_request=vehicle_request, vehicle=vehicle, is_active=True
                )
                vehicle.is_available = False
                vehicle.save()
            messages.success(request, "You have successfully assigned vehicles")
            return render(
                request, "admin/request/assign_driver_detail.html", context=context
            )
        else:
            print(form.errors)
            return render(
                request, "admin/request/assign_driver_detail.html", context=context
            )


class SendSMSforVehicleRequestView(LoginRequiredMixin, View):
    def post(self, request, vehicle_id):
        v_id_from_form = request.POST.getlist("vehicle")
        print(v_id_from_form)
        vehicle_request = get_object_or_404(VehicleBooking, id=vehicle_id)
        assigned_vehicle_ids = AssignedVehicle.objects.filter(
            vehicle_request=vehicle_id
        ).values_list("vehicle__id", flat=True)
        vehicle = VehicleData.objects.filter(
            is_available=True, is_expired=True
        ).exclude(id__in=assigned_vehicle_ids)
        assigned = AssignedVehicle.objects.filter(
            vehicle_request=vehicle_request, is_terminated=False
        )  # .select_related('vehicle').prefetch_related('vehicle__images')
        form = AssignedVehicleForm(
            request.POST or None,
            vehicles=vehicle,
            initial={"vehicle_request": vehicle_request.id, "vehicle": vehicle},
        )
        context = {
            "form": form,
            "object": vehicle_request,
            "vehicles": vehicle,
            "assigned": assigned,
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Vehicle Assign Update",
        }
        if form.is_valid():
            current_site = get_current_site(request)
            selected_vehicle_ids = form.cleaned_data["vehicle"]
            selected_vehicles = VehicleData.objects.filter(id__in=v_id_from_form)
            for vehicle in selected_vehicles:
                link = f"{current_site.domain}/api/accounts/assign/verify/sms/{vehicle_request.id}/{vehicle.plate_number}/"
                message = f" ዉድ ደንበኛችን በ {vehicle.plate_number} ታርጋ ቁጥር አዲናስ ካር ሬንት ጋር ያስመዝገቡት ተሽከርካሪ ለስራ"
                f" ከ ቀን {vehicle_request.start_date} እስከ {vehicle_request.end_date}"
                f" ከ {vehicle_request.pickup} ወደ {vehicle_request.drop_off}"
                f" ለ {vehicle_request.duration} ቀን ያለ አሽከርካሪ ስለተፈለገ "
                f"በቀን ሂሳብ {vehicle_request.daily_price} ብር ከተስማሙ ከዚህ  በታች ያለዉን ሊንክ በመጫን መስማማትዎን በማረጋገጥ ስራ መጀመር ይችላሉ።"
                f"{link} \n"
                f" ለተጨማሪ ጥያቄ በ +251911323333 ይደዉሉ። Adinas Car Rent Team"

                sms_api_router(vehicle.account.phone_number, message)
            messages.success(request, f"You have successfully send SMS")
            return render(
                request, "admin/request/assign_driver_detail.html", context=context
            )
        else:
            print(form.errors)
            return render(
                request, "admin/request/assign_driver_detail.html", context=context
            )


class SendInAppforVehicleRequest(LoginRequiredMixin, View):
    def post(self, request, vehicle_id):
        try:
            v_id_from_form = request.POST.getlist("vehicle")
            # print(v_id_from_form)
            vehicle_request = get_object_or_404(VehicleBooking, id=vehicle_id)
            # assigned_vehicle_ids = AssignedVehicle.objects.filter(vehicle_request=vehicle_id).values_list('vehicle__id', flat=True)
            # vehicle = VehicleData.objects.filter(is_available=True,is_expired=True).exclude(id__in=assigned_vehicle_ids)
            # assigned = AssignedVehicle.objects.filter(vehicle_request=vehicle_request, is_terminated=False)#.select_related('vehicle').prefetch_related('vehicle__images')

            selected_vehicles = VehicleData.objects.filter(id__in=v_id_from_form)
            for vehicle in selected_vehicles:
                devices = FCMDevice.objects.filter(user=vehicle.account)
                if devices.exists():
                    for device in devices:
                        print(device)
                        device.send_message(
                            Message(data={
                                    "pickup": str(vehicle_request.pickup),
                                    "destination": str(vehicle_request.drop_off),
                                    "duration": str(vehicle_request.duration),
                                    "start_date": str(
                                        vehicle_request.start_date
                                    ),
                                    "end_date": str(vehicle_request.end_date),
                                    "plate_number":str(vehicle.plate_number)
                                })
                        )
                        devices.send_message(
                            Message(
                                notification=Notification(
                                    title="You have a new Trip Request",
                                    body="በ ታርጋ ቁጥር {} የተመዘገበዉ መኪና ከ {} ወደ {} ለ {} ቀን ስለተፈለገ በ ስልክ ቁጥር +251911510313 ደዉለው ያነጋግሩን። Adinas Car Rent Team.".format(
                                        vehicle.plate_number,
                                        vehicle_request.pickup,
                                        vehicle_request.drop_off,
                                        vehicle_request.duration + 1 if vehicle_request.duration == 0 else vehicle_request.duration,
                                    ),
                                )
                            )
                        )
            messages.success(
                self.request, f"You have successfully Sent In app notification"
            )
            return redirect("admin:assign_request", vehicle_id=vehicle_id)
        except Exception as e:
            messages.warning(self.request, str(e))
            return redirect("admin:assign_request", vehicle_id=vehicle_id)


class AssignVehicleBooking(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            vehicle_booking = VehicleBooking.objects.get(id=kwargs["pk"])
            vehicles = VehicleData.objects.filter(
                available=True,
                service_type__id=vehicle_booking.vehicle_type.id,
                working=False,
                expired=False,
            ).exclude(requested_vehicle__vehicle_request=vehicle_booking)
            if vehicle_booking.brand != None:
                vehicles = vehicles.filter(brand__id=vehicle_booking.brand.id)
            if vehicle_booking.model != None:
                vehicles = vehicles.filter(model__id=vehicle_booking.model.id)
            if vehicle_booking.vehicle_type != None:
                vehicles = vehicles.filter(type__id=vehicle_booking.vehicle_type.id)
            if vehicle_booking.production_year != None:
                vehicles = vehicles.filter(
                    production_year__year__gte=vehicle_booking.production_year.year
                )

            context = {
                "subtitle": "Assign Vehicles to a Request",
                "option": kwargs["option"],
                "vehicles": vehicles,
                "object": vehicle_booking,
            }
            return render(
                self.request, "admin/pages/order/assign_vehicle.html", context
            )
        except Exception as e:
            return render(self.request, "admin/widgets/500.html", {"message": e})

    def post(self, *args, **kwargs):
        try:
            vehicle_request = VehicleBooking.objects.get(id=kwargs["pk"])
            vehicle_request.order_daily_price = self.request.POST["price"]
            # vehicle_request.distance_radius = self.request.POST["distance_radius"]
            vehicle_request.dispatched = True
            vehicle_request.save()

            vehicle_id = self.request.POST["vehicles"].split(",")

            vehicles = VehicleData.objects.filter(id__in=vehicle_id)

            for vehicle in vehicles:
                if vehicle not in vehicle_request.assigned_vehicles():
                    # TODO: assign vehicle here.....
                    pass
            messages.success(self.request, "You have successfully assigned vehicles")
            return redirect(
                "admin:order_detail",
                detail="vehicles",
                option=kwargs["option"],
                pk=kwargs["pk"],
            )
        except Exception as e:
            return render(self.request, "admin/widgets/500.html", {"message": e})


class SendTelegramforVehicleRequestView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        vehicle_id = self.kwargs["vehicle_id"]
        vehicle_request = get_object_or_404(VehicleBooking, id=vehicle_id)
        try:
            send_telegram_message(
                f"ዉድ ደንበኛችን ከ ቀን {vehicle_request.start_date} እስከ {vehicle_request.end_date}"
                f" ከ {vehicle_request.pickup} ወደ {vehicle_request.drop_off}"
                f" ለ {vehicle_request.duration} ቀን ያለ አሽከርካሪ ስለተፈለገ "
                f"መስራት ከፈለጉ ከዚህ በታች ወዳለዉ ስልክ በመደወል ስራ መጀመር ይችላሉ።\n"
                f"ስልክ፡ +251911323333 ይደዉሉ። \n\nAdinas Car Rent Team"
            )

            messages.success(self.request, f"You have successfully Posted on telegram")
            return redirect("admin:assign_request", vehicle_id=vehicle_id)
        except Exception as e:
            print(e)
            return redirect("admin:assign_request", vehicle_id=vehicle_id)


class RemoveAssignVehicleToVehicleRequestView(LoginRequiredMixin, View):

    def post(self, request, vehicle_id, v_id):
        vehicle_request = get_object_or_404(VehicleBooking, id=vehicle_id)
        vehicle = get_object_or_404(VehicleData, id=v_id)
        redirect_url = reverse(
            "admin:assign_request", kwargs={"vehicle_id": vehicle_id}
        )

        AssignedVehicle.objects.filter(
            vehicle_request=vehicle_request, vehicle=vehicle
        ).update(is_terminated=True)
        vehicle.is_available = True
        vehicle.save()
        messages.success(request, "Assigned Vehicle Removed  successfully")
        return redirect(redirect_url)


class GetAllVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request):
        drives = VehicleBooking.objects.filter(is_expired=False)
        context = {
            "vehicle_data": drives,
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Vehicle Request List",
        }
        return render(request, "admin/request/request_list.html", context=context)


class GetAllExpiredVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request):
        drives = VehicleBooking.objects.filter(is_expired=True)
        context = {
            "vehicle_data": drives,
            "archive": "active",
            "archive_submenu": "active",
            "subtitle": "Expired Vehicle Request List",
        }
        return render(request, "admin/recycle/request_list.html", context=context)


class GetOneVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        driver = get_object_or_404(VehicleBooking, id=vehicle_id)
        form = VehicleBookingForm()
        context = {
            "requests": "active",
            "requests_submenu": "active",
            "subtitle": "Vehicle Request Detail",
            "page_title": "Update Vehicle Request Detail",
            "object": driver,
            "form": form,
        }
        return render(request, "admin/request/request_detail.html", context=context)


class DeleteVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        drive = get_object_or_404(VehicleBooking, id=vehicle_id)
        drive.delete()
        messages.success(request, "Vehicle Request Deleted successfully")
        return redirect("admin:get_all_request")


class ExpireVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        drive = get_object_or_404(VehicleBooking, id=vehicle_id)
        drive.is_expired = not drive.is_expired
        drive.save()
        message = f'Vehicle Request {"Removed" if drive.is_expired else "Restored"} successfully'
        messages.success(request, message)
        url = (
            "admin:recycle_all_request"
            if not drive.is_expired
            else "admin:get_all_request"
        )
        return redirect(url)


class ActivateDeactivateVehicleRequestView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        drive = get_object_or_404(VehicleBooking, id=vehicle_id)
        drive.is_active = not drive.is_active
        drive.save()
        message = f'Vehicle Request {"Activated" if drive.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_request")
