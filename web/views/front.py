from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from accounts.models import UserAccount
from booking.models import VehicleBooking
from vehicle.models import VehicleData

from web.models import About, Partner, Service, Slider, Testimonal, Message
from web.forms import MessageForm

# Create your views here.
class WebIndexView(View):
    def get(self, request):
        form =  MessageForm()
        slider = Slider.objects.filter(is_active=True).order_by("-created_at")
        about = About.objects.filter(is_active=True).latest("created_at")
        services = Service.objects.filter(is_active=True).order_by("-created_at")
        testimonials = Testimonal.objects.filter(is_active=True).order_by("-created_at")
        partners = Partner.objects.filter(is_active=True).order_by("-created_at")
        users = UserAccount.objects.filter(is_staff=False)
        vehicles = VehicleData.objects.all().count()
        booking = VehicleBooking.objects.all().count()
        facts = {
            "clients":users.filter(is_client=True).count(), 
            "fleets":vehicles,
            "rentals":booking
        }
        context = {
            "sliders": slider,
            "form":form,
            "about": about,
            "services": services,
            "testimonials": testimonials,
            "partners": partners,
            "facts":facts
        }
        return render(request, 'website/index.html', context=context)


