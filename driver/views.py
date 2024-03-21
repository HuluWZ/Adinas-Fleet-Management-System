from django.shortcuts import redirect, render ,get_object_or_404
# Create your views here.
# create form for the model Driver        
from .models import Driver
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Driver , Owner
from accounts.models import UserAccount
from .forms import DriverForm ,OwnerForm  # Assuming you have a form defined for Drive model
from os.path import splitext

class CreateDriveView(LoginRequiredMixin,View):
    def get(self, request):
        form = DriverForm()  # Create an instance of your form
        context ={
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Add Driver",
            'page_title':"Add Driver Form",
            'form':form
        }
        return render(request, 'admin/driver/driver_form.html', context=context)
    def post(self,*arts,**kwargs):
        form = DriverForm(self.request.POST,self.request.FILES)
        if form.is_valid():
           newdriver = form.save(commit=False)
           role = form.cleaned_data.get('role')
           if role == 'driver':
                newdriver.is_driver = True
           elif role == 'owner':
                newdriver.is_owner = True
           elif role == 'both':
                newdriver.is_both = True
           newdriver.created_by=self.request.user
           newdriver.save()
           driver_obj = Driver.objects.create(
               account=newdriver,
               created_by=self.request.user
            )
            
           messages.success(self.request,"Driver Added successfully")
           return redirect("admin:get_all_drivers")
        else:
            context = {           
              'drivers':'active',
              'drivers_submenu':'active',
              'subtitle':"Add Driver",
              'page_title':"Add Driver Form",
              'form':form
             }
            return render(self.request,"admin/driver/driver_form.html",context=context)


class UpdateDriveView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        driver = get_object_or_404(Driver, id=driver_id)
        form = DriverForm(instance=driver.account)  
        context = {
            'form': form ,
            'object':driver,
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Driver Driver",
        }
        return render(request, 'admin/driver/driver_detail.html', context=context)
    def post(self, request, driver_id):
        drive = get_object_or_404(Driver, id=driver_id)
        form = DriverForm(request.POST,request.FILES,instance=drive.account)
        if form.is_valid():
            drive = form.save(commit=False)
            role = form.cleaned_data.get('role')
            if role == 'driver':
                drive.is_driver = True
                drive.is_owner = False
                drive.is_both = False
            elif role == 'owner':
                drive.is_owner = True
                drive.is_driver = False
                drive.is_both = False
            elif role == 'both':
                drive.is_both = True
                drive.is_owner = False
                drive.is_driver = False

            drive.created_by=self.request.user
            drive.save()
            messages.success(request,"Driver Updated successfully")
            return redirect("admin:get_all_drivers")
        else:
            context = {
               'form': form ,
               'object':drive,
               'drivers':'active',
               'drivers_submenu':'active',
               'subtitle':"Driver Update",
              }
            return render(request, 'admin/driver/driver_detail.html', context=context)



class GetAllDrivesView(LoginRequiredMixin,View):
    def get(self, request):
        drives = Driver.objects.filter(is_expired=False)
        context = {
            'drives_data': drives ,
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Drivers List",
        }
        return render(request,"admin/driver/driver_list.html",context=context)

class GetAllExpiredDrivesView(LoginRequiredMixin,View):
    def get(self, request):
        drives = Driver.objects.filter(is_expired=True)
        context = {
            'drives_data': drives ,
            'archive':'active',
            'archive_submenu':'active',
            'subtitle':"Expired Drivers List",
        }
        return render(request,"admin/recycle/driver_list.html",context=context)

class GetOneDriveView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Driver, id=driver_id)
        form = DriverForm()  # Create an instance of your form
        context =  {
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Driver Detail",
            'page_title':"Update Driver Detail",
            'object':drive,
            'form':form
        }
        return render(request,"admin/driver/driver_detail.html",context=context)

class DeleteDriveView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Driver, id=driver_id)
        drive.delete()
        messages.success(request,"Driver Deleted successfully")
        return redirect("admin:get_all_drivers")
    
class ExpireDriverView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Driver, id=driver_id)
        drive.is_expired = not drive.is_expired
        drive.save()
        message = f'Driver {"Removed" if drive.is_expired else "Restored"} successfully'
        url = "admin:recycle_all_drivers" if not drive.is_expired else "admin:get_all_drivers"
        messages.success(request, message)
        return redirect(url)
    
class ActivateDeactivateDriveView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Driver, id=driver_id)
        drive.is_active = not drive.is_active
        drive.save()
        message = f'Driver {"Activated" if drive.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_drivers")   



class CreateOwnerView(LoginRequiredMixin,View):
    def get(self, request):
        form = OwnerForm()  
        context ={
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Add Owner",
            'page_title':"Add Owner Form",
            'form':form
        }
        return render(request, 'admin/owner/owner_form.html', context=context)
    def post(self,*arts,**kwargs):
        form = OwnerForm(self.request.POST,self.request.FILES)
        if form.is_valid():
           newdriver = form.save(commit=False)
           role = form.cleaned_data.get('role')
           if role == 'driver':
                newdriver.is_driver = True
           elif role == 'owner':
                newdriver.is_owner = True
           elif role == 'both':
                newdriver.is_both = True
           newdriver.created_by=self.request.user
           newdriver.save()
           driver_obj = Owner.objects.create(
               account=newdriver,
               created_by=self.request.user
            )
            
           messages.success(self.request,"Owner Added successfully")
           return redirect("admin:get_all_owners")
        else:
            context = {           
              'drivers':'active',
              'drivers_submenu':'active',
              'subtitle':"Add Owner",
              'page_title':"Add Owner Form",
              'form':form
             }
            return render(self.request,"admin/owner/owner_form.html",context=context)



class UpdateOwnerView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        driver = get_object_or_404(Owner, id=driver_id)
        form = OwnerForm(instance=driver.account)  
        context = {
            'form': form ,
            'object':driver,
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Owner Update",
        }
        return render(request, 'admin/owner/owner_detail.html', context=context)
    def post(self, request, driver_id):
        drive = get_object_or_404(Owner, id=driver_id)
        form = OwnerForm(request.POST,request.FILES,instance=drive.account)
        if form.is_valid():
            drive = form.save(commit=False)
            role = form.cleaned_data.get('role')
            if role == 'driver':
                drive.is_driver = True
                drive.is_owner = False
                drive.is_both = False
            elif role == 'owner':
                drive.is_owner = True
                drive.is_driver = False
                drive.is_both = False
            elif role == 'both':
                drive.is_both = True
                drive.is_owner = False
                drive.is_driver = False

            drive.created_by=self.request.user
            drive.save()
            messages.success(request,"Owner Updated successfully")
            return redirect("admin:get_all_owners")
        else:
            context = {
               'form': form ,
               'object':drive,
               'drivers':'active',
               'drivers_submenu':'active',
               'subtitle':"Owner Update",
              }
            return render(request, 'admin/owner/owner_detail.html', context=context)


class GetAllOwnerView(LoginRequiredMixin,View):
    def get(self, request):
        drives = Owner.objects.filter(is_expired=False)
        context = {
            'drives_data': drives ,
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Owners List",
        }
        return render(request,"admin/owner/owner_list.html",context=context)

class GetAllExpiredOwnerView(LoginRequiredMixin,View):
    def get(self, request):
        drives = Owner.objects.filter(is_expired=True)
        context = {
            'drives_data': drives ,
            'archive':'active',
            'archive_submenu':'active',
            'subtitle':"Expired Owners List",
        }
        return render(request,"admin/recycle/owner_list.html",context=context)

class GetOneOwnerView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Owner, id=driver_id)
        form = OwnerForm()  # Create an instance of your form
        context =  {
            'drivers':'active',
            'drivers_submenu':'active',
            'subtitle':"Owner Detail",
            'page_title':"Update Owner Detail",
            'object':drive,
            'form':form
        }
        return render(request,"admin/owner/owner_detail.html",context=context)

class DeleteOwnerView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Owner, id=driver_id)
        drive.delete()
        messages.success(request,"Owner Deleted successfully")
        return redirect("admin:get_all_owners")
 
class ExpireOwnerView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Owner, id=driver_id)
        drive.is_expired = not drive.is_expired
        drive.save()
        message = f'Owner {"Removed" if drive.is_expired else "Restored"} successfully'
        messages.success(request, message)
        url = "admin:recycle_all_owners" if not drive.is_expired else "admin:get_all_owners"
        return redirect(url)
   
class ActivateDeactivateOwnerView(LoginRequiredMixin,View):
    def get(self, request, driver_id):
        drive = get_object_or_404(Owner, id=driver_id)
        drive.is_active = not drive.is_active
        drive.save()
        message = f'Owner {"Activated" if drive.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_owners")   

