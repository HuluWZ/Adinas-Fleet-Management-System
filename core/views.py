from django.shortcuts import render
from django.views.generic import (View)
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import *
from client.models import Client
from driver.models import Driver , Owner
from vehicle.models import VehicleData
from django.db.models.functions import ExtractMonth ,ExtractYear
from datetime import datetime
from driver.models import Driver ,Owner
from booking.models import VehicleBooking
from django.db.models import Count
def handler404(request,exception):
    return render(request, 'admin/widgets/404.html', status=404)

def handler500(request):
    return render(request, 'admin/widgets/500.html', status=500)

def percentage_of_available_vehicle(year=None):
    aggregates = VehicleData.objects.filter(
        created_at__year=year
    ).aggregate(
        not_available_count=Count('pk', filter=models.Q(is_available=True)),
        total_count=Count('pk'),
    )
    not_available_models_count = aggregates['not_available_count']
    total_models_count = aggregates['total_count']
    percentage = round((not_available_models_count / total_models_count) * 100) if total_models_count > 0 else 0
    return percentage

def monthly_count_report(model,year=None):
         
    monthly_counts = model.objects.filter(created_at__year=year) \
        .annotate(month=ExtractMonth('created_at')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    vehicle_counts = [0] * 12  

    for entry in monthly_counts:
        month = entry['month'] - 1  
        vehicle_counts[month] = entry['count']
    return vehicle_counts

class IndexView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            current_year = datetime.now().year
            years = list(range(2020, current_year + 1))[::-1]
            selected_year = int(self.request.GET.get('year', current_year))
            
            if selected_year:
                year = selected_year
            else:
                year = current_year
            
            default_year = selected_year if selected_year  else current_year

            client = Client.objects.all().count()
            vehicle = VehicleData.objects.all().count()
            driver = Driver.objects.all().count()
            owner = Owner.objects.all().count()
            vehicle_count = monthly_count_report(VehicleData,year=year)
            vehicle_booking_count = monthly_count_report(VehicleBooking,year=year)
            driver_count = monthly_count_report(Driver,year=year)
            owner_count = monthly_count_report(Owner,year=year)
            percentage = percentage_of_available_vehicle(year=year)
            context = {
                      'subtitle':"Home",
                       "client":client,
                       "vehicle":vehicle,
                       "driver":driver,
                       "owner":owner,
                       "vehicle_count":vehicle_count,
                       "vehicle_booking_count":vehicle_booking_count,
                       "driver_count":driver_count,
                       "owner_count":owner_count,
                       "percentage":percentage,
                       "years":years,
                       "selected_year":default_year
            }                                        
            return render(self.request,"admin/index.html",context=context)
        except Exception as e:
            return render(self.request,"admin/widgets/500.html",{'message':"Hint: "+str(e)})



class ArchiveList(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {
            'subtitle':"Archives",
            'users':{
                'archived':UserAccount.objects.filter(expired=True).count(),
                "total":UserAccount.objects.all().count()
                },
            }
        return render(self.request,"admin/core/archives.html",context=context)


class ArchiveDetail(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {
            'subtitle': self.kwargs['archive_type']+" Archive",
            'archive_type':self.kwargs['archive_type']
            }
        
        return render(self.request,"admin/core/archive_detail.html",context=context)

class RemoveAll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            return render(self.request,"admin/widgets/404.html",{
                    'message':"Hint: You somehow have managed to change the request parameter"})
        except Exception as e:
            return render(self.request,"admin/widgets/500.html",{'message':"Hint: "+str(e)})

        
class RestoreArchive(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            return render(self.request,"admin/widgets/404.html",{
            'message':"Hint: You somehow have managed to change the request parameter"})
        except Exception as e:
            return render(self.request,"admin/widgets/500.html",{'message':"Hint: "+str(e)})
