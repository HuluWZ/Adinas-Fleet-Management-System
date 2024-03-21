from base64 import urlsafe_b64decode
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse, Http404
from django.contrib import messages
from django.views.generic import (CreateView,View,UpdateView,ListView)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission,Group
from accounts.email_messages import sendEmailVerification, sendWelcomeEmail
from accounts.forms import *
import pyotp
from utils.sms_messages import sms_api_router
from .authentication import JWTAuthentication
from  vehicle.forms import VehicleForm ,VehicleWebForm , VehicleImageForm
from vehicle.models import VehicleData, VehicleImage
from django.contrib.auth.decorators import login_required 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import login , authenticate
from .forms import UserSignupWebForm
from web.forms import MessageForm
from web.models import Message
from django.db.models import Q , Count


class UpdateVehicleImageView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        images = VehicleImage.objects.filter(vehicle=vehicle).order_by("-created_at").all()
        form = VehicleImageForm()  
        context = {
            "form": form,
            "object": vehicle,
            "images": images,
        }
        return render(request, "website/vehicle_detail.html", context=context)

class RemoveVehicleImage(LoginRequiredMixin, View):
    
    def get(self,request,image_id):
        image = get_object_or_404(VehicleImage, id=image_id)
        image.delete()
        messages.success(request, "Vehicle Image Deleted successfully")
        return redirect("my_vehicle")


class UpdateVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        images = VehicleImage.objects.filter(vehicle=vehicle).order_by('-created_at').all()
        has_images = images.exists()
        form = VehicleWebForm(instance=vehicle)
        form2 = VehicleImageForm()  
        context = {
            "form": form,
            "form2":form2,
            "object": vehicle,
            "images": images,
            "has_images": has_images,
        }
        return render(request, "website/vehicle_detail.html", context=context)

    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        images = VehicleImage.objects.filter(vehicle=vehicle)
        has_images = images.exists()
        form = VehicleWebForm(request.POST, request.FILES, instance=vehicle)
        form2 = VehicleImageForm()
        if 'submit_form1' in request.POST:
          if form.is_valid():
            form.save()
            messages.success(request, "Vehicle Updated successfully")
            return redirect("my_vehicle")
          else:
            context = {
                "form": form,
                "form2": form2,
                "images": images,
                "has_images": has_images,
                "object": vehicle,
            }
            return render(request, "website/vehicle_detail.html", context=context)
        if 'submit_form2' in request.POST:
           form = VehicleImageForm(request.POST,request.FILES)
           uploaded_images = request.FILES.getlist("image")
           if uploaded_images:
             uploaded_images = request.FILES.getlist("image")
             for image in uploaded_images:
                new_vehicle_image = VehicleImage(vehicle=vehicle, image=image)
                new_vehicle_image.save()
             messages.success(request, f" {len(uploaded_images)} Vehicle Image Uploaded successfully")
             return redirect('update_vehicle', vehicle_id=vehicle_id)
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
            return render(request, "website/vehicle_detail.html", context=context)


class DeleteVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(VehicleData, id=vehicle_id)
        vehicle.delete()
        messages.success(request, "Vehicle Deleted successfully")
        return redirect("my_vehicle")


class ActivateDeactivateVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        client = get_object_or_404(VehicleData, id=vehicle_id)
        client.is_active = not client.is_active
        client.is_available = not client.is_available
        client.save()
        message = (
            f'Vehicle {"Activated" if client.is_available else "Deactivated"} successfully'
        )
        messages.success(request, message)
        return redirect("my_vehicle")

class CreateMessageView(View):
    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Message Sent successfully")
            return redirect("web_index")
        else:
            context = {
              'form': form ,
            }
            return render(request, 'website/index.html', context=context)

def signup(request):
    if request.method == 'GET':
        form = UserSignupWebForm()
        context = {"form": form}
        return render(request, "website/signup.html", context=context)

    elif request.method == 'POST':
        form = UserSignupWebForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            role = form.cleaned_data.get('role')
            user = form.save(commit=False)
            user.username = phone_number
            role = form.cleaned_data.get('role')
            if role == 'driver':
                    user.is_driver = True
            elif role == 'owner':
                    user.is_owner = True
            elif role == 'both':
                    user.is_both = True
            otp_secret = pyotp.random_base32()
            user.otp_secret = otp_secret
            user.save()
            request.session['phone_number'] = phone_number
            otp = pyotp.TOTP(otp_secret, interval=2000)
            generated_otp = otp.now()
            messages.success(request, "Account Created successfully & Check The OTP. ")
            sms_api_router(phone_number, f"Your Adinas Car Rent App verification OTP is {generated_otp}")
            return redirect('verify_otp')
        else:            
            phone_number = request.POST.get('phone_number')
            try:
              user_account = UserAccount.objects.filter(phone_number=phone_number).first()
              otp_secret = user_account.otp_secret
              otp = pyotp.TOTP(otp_secret, interval=2000)
              generated_otp = otp.now()
              sms_api_router(phone_number, f"Your Adinas Car Rent App verification OTP is {generated_otp}")
              request.session['phone_number'] = phone_number
              messages.success(request, "OTP has been sent. Please check your phone.")
              return redirect('verify_otp')
            except ObjectDoesNotExist:
              messages.error(request, "User with this phone number does not exist.")
              return redirect('signup')

    

class GetMyVehicle(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        vehicles = VehicleData.objects.filter(account=user)
        ignore_register = UserAccount.objects.filter(id=user.id).annotate(vehicle_count=Count('vehicle')).filter(
            Q(is_driver=True) & Q(vehicle_count__gt=0)
        ).exists()
        context = {
            "vehicle_data": vehicles,
            "ignore_register":ignore_register
        }
        return render(request, "website/vehicle_list.html", context=context)

class WebMyProfileView(LoginRequiredMixin,UpdateView):
    model = UserAccount
    form_class = AFMSUserProfileForm
    template_name = "website/profile.html"
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self,form):
        user = form.save()
        user.last_updated_date=timezone.now()
        user.last_updated_by=self.request.user
        user.save()
        messages.success(self.request,"Your Profile Updated Successfully")
        context = {'form':form,'object':user,'error':False,'message':"Your Profile Updated Successfully",'subtitle':"My Profile"}
        return render(self.request,"website/profile.html",context=context)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_invalid(self,form):
        context = {'form':form,'object':self.request.user,'error':True,'message':"Error updating","subtitle":"My Profile"}
        return render(self.request,"website/profile.html",context=context)

def create_vehicle_from_view(request):
    if request.method == 'GET':
        form = VehicleWebForm()
        context = {"form": form}
        return render(request, "website/vehicle_form.html", context=context)

    elif request.method == 'POST':
        form = VehicleWebForm(request.POST, request.FILES)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.account = request.user
            vehicle.created_by = request.user
            selected_areas_of_interest = form.cleaned_data['area_of_interests'].values_list('id', flat=True)
            vehicle.save()
            
            for selected_area in selected_areas_of_interest:  
              vehicle.area_of_interests.add(selected_area)

            images = request.FILES.getlist("vehicle_images")
            for image in images:
                VehicleImage.objects.create(vehicle=vehicle, image=image)
            messages.success(request, "Vehicle Registered successfully")
            return redirect('my_vehicle')
        
        else:
            print(" Error ",form.errors)
            form = VehicleWebForm()
            context = {"form": form}
            return render(request, "website/vehicle_form.html", context=context)


def send_otp(request):
    user = request.user.is_authenticated
    token = request.session.get('token')
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = UserAccount.objects.get(phone_number=phone_number)

            except UserAccount.DoesNotExist:
                messages.warning(request, 'User not found. Please check the phone number.')
                return redirect('send_otp')
            otp_secret = pyotp.random_base32()
            user.otp_secret = otp_secret
            user.save()
            otp = pyotp.TOTP(otp_secret, interval=2000)
            generated_otp = otp.now()
            request.session['phone_number'] = phone_number
            sms_api_router(phone_number,f"Your Adinas Car Rent App verification OTP is {generated_otp}")
            messages.success(request,f"OTP Send to {phone_number} Successfully.")
            return redirect('verify_otp')

    else:
        if user:  
            return redirect('register_vehicle')
        else:
          form = PhoneNumberForm()
          return render(request, 'website/login.html',{"form":form})

def verify_otp(request):
    phone_number = request.session.get('phone_number')
    if not phone_number :
        return redirect('send_otp')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request,request.POST)
        print("Form Fields:", form.fields)

        if form.is_valid():
            messages.success(request,"User Logged in Successfully!")
            return redirect("web_index")
        print(" Login Error ",form.errors)
        messages.warning(request,"OTP Authentication Failed. Try Again!.")
        return redirect("send_otp")
    else:
        form = CustomAuthenticationForm()
        return render(request, 'website/verify.html', {'form': form})

class AFMSUserSignUpView(CreateView):
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request,"You Already have Account,Please logout and create an account")
            return redirect("admin:index")
        else:
            form = AFMSUserSignUpForm()
            return render(self.request,'admin/accounts/signup.html',{"form":form})
     
    def post(self, *args,**kwargs):
        try:
            form = AFMSUserSignUpForm(self.request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
                # sendEmailVerification(self.request,user)
                print(" email sent ",self.request);
                return render(self.request,'messages/confirm_registration_message.html',
                    {'message':"Verification Email is Sent,\nPlease Verify your email address to complete the registration\n"
                    +"If you can\'t find the mail please check it in your spam folder!",'user_to_activate':user})
            else:
                return render(self.request,'admin/accounts/signup.html',{'form':form})
        except Exception as e:
            return render(self.request,"admin/widgets/500.html",{'message':e})

def send_verification_email(request,request_user):
    try:
        user = UserAccount.objects.get(id=request_user)
        result = sendEmailVerification(request,user)
        return render(request,'messages/confirm_registration_message.html',
                {'message':"Verification Email is Sent,\n Please Verify your email address to complete the registration\n"
                +"If you can\'t find the mail please check it in your spam folder!",'user_to_activate':user})
    except UserAccount.DoesNotExist:
        return render(request,"admin/widgets/404.html")
    except Exception as e:
        user = UserAccount.objects.get(id=request_user)
        print(e)
        return render(request,'messages/confirm_registration_message.html',
                {'message':"Verification Email is Not Sent, Please Try Again!!",'user_to_activate':user})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserAccount.DoesNotExist) as e:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        sendWelcomeEmail(request,user)
        return render(request,'messages/confirm_registration_message.html',
        {'tags':"success",'message':"Thank you for your email confirmation. Now you can login to your account.",'url':True})
    else:
        return render(request,'messages/confirm_registration_message.html',
        {'tags':"warning",'message':"Activation link is invalid!"})



class MyProfileView(LoginRequiredMixin,UpdateView):
    model = UserAccount
    form_class = AFMSUserProfileForm
    template_name = "admin/accounts/profile.html"

    def form_valid(self,form):
        user = form.save()
        user.last_updated_date=timezone.now()
        user.last_updated_by=self.request.user
        user.save()
        messages.success(self.request,"Your Profile Updated Successfully")
        context = {'form':form,'object':user,'error':False,'message':"Your Profile Updated Successfully",'subtitle':"My Profile"}
        return render(self.request,"admin/accounts/profile.html",context=context)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = "My Profile"
        print(" Context = ",context)
        return context
    
    def form_invalid(self,form):
        print(" Invalid")
        context = {'form':form,'object':self.request.user,'error':True,'message':"Error updating","subtitle":"My Profile"}
        return render(self.request,"admin/accounts/profile.html",context=context)


# to list all users in the admin page

class UserListView(LoginRequiredMixin, ListView):
    model=UserAccount
    template_name = "admin/accounts/users_list.html"
    
    def get_queryset(self):
        return UserAccount.objects.filter(expired=False).exclude(id=self.request.user.id)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = "Users List"
        return context

# to see a users detail profile

class UserDetailView(LoginRequiredMixin, UpdateView):
    model = UserAccount
    form_class = AFMSUserUpdateForm
    template_name = "admin/accounts/user_detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = "User Detail"
        return context

    def form_valid(self,form):
        user_profile = form.save()
        user_profile.last_updated_date=timezone.now()
        user_profile.last_updated_by=self.request.user
        user_profile.save()
        messages.success(self.request,"User Info Updated Successfully")
        # context = {'object':user_profile,'form':form,'error':False}
        # context['subtitle'] = "User Detail"
        # return render(self.request,"admin/accounts/user_detail.html",context=context)
        return redirect("admin:users_list")

    def form_invalid(self,form):
        
        context = {'object':UserAccount.objects.get(id=self.kwargs['pk']),
                    'form':form,'subtitle':'User Detail','error':True,"message":form.errors}
        return render(self.request,"admin/accounts/user_detail.html",context=context)


class ChangeUserPassword(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        template_name = "admin/accounts/password_form.html"
        context = {
            'subtitle':"Change User Password",
            'form':UserPasswordChangeForm(),
            'object':UserAccount.objects.get(id=self.kwargs['pk'])
        }
        return render(self.request,template_name,context)
    
    def post(self,*args,**kwargs):
        form = UserPasswordChangeForm(self.request.POST)
        if form.is_valid():
            try:
                user = UserAccount.objects.get(id=kwargs['pk'])
                user.set_password(form.cleaned_data.get("password1"))
                user.last_updated_by=self.request.user
                user.last_updated_date=timezone.now()
                user.save()
                messages.success(self.request,"Password for User {} Changed .".format(user.username))
                return redirect("admin:users_list")
            except Exception as e:
                messages.warning(self.request,e)
                return redirect("admin:users_list")
        else:
            return render(self.request,"admin/accounts/password_form.html",{
                'form':form,'object':UserAccount.objects.get(id=kwargs['pk'])
            })

class SuspendUser(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            user = UserAccount.objects.get(id=self.kwargs['pk'])
            if self.kwargs['option'] == "suspend":
                user.is_active = False
                user.save()
                messages.success(self.request,"User Suspended")
                return redirect("admin:users_list")
            elif self.kwargs['option'] == 'enable':
                user.is_active = True
                user.save()
                messages.success(self.request,"User Activated")
                return redirect("admin:users_list")
            
        except UserAccount.DoesNotExist:
            messages.success(self.request,"The User Does Not Exist")
            return redirect("admin:users_list")



class CreateCompanyStaff(LoginRequiredMixin,CreateView):
    model=UserAccount
    form_class = AFMSUserCreationForm
    template_name = "admin/accounts/user_form.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = "User Profile form"
        return context

    def form_valid(self,form):
        user = form.save()
        user.created_by = self.request.user
        user.save()
        context = {
            'error':False,
            'message':"You Created a User Successfully!",
            "object_list":UserAccount.objects.all().exclude(id=self.request.user.id)
        }
        messages.success(self.request,"You Created a User Successfully!")
        return render(self.request,"admin/accounts/users_list.html",context=context)

    def form_invalid(self, form):
        return render(self.request,"admin/accounts/user_form.html", {'form':form,'message':form.errors} )

class GroupList(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            groups = Group.objects.all()
            permission_id = []
            current_group = None
            
            if groups.count() > 0:
                current_group = groups[0]
                for existing in groups[0].permissions.all():
                    permission_id.append(existing.id)
            context = {'existing_permissions':Permission.objects.all().exclude(id__in=permission_id),
                        "groups":groups,'current_group':current_group,"subtitle":"User Role List"}
            return render(self.request,"admin/accounts/group_list.html",context=context)      
        except Exception as e:
            print(e)
            return render(self.request,"admin/widgets/500.html",{'message':"Hint: "+str(e)})




class GroupView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            permissions = Permission.objects.all()
            return render(self.request,"admin/accounts/group_form.html",{'permisions':permissions,"subtitle":"User Role Form"})
        except Exception as e:
            return render(self.request,"admin/widgets/500.html",{'message':"Hint: "+str(e)})

    def post(self,*args,**kwargs):
        try:
            permission_list = []
            for permision_id in self.request.POST.getlist('sel_perm_list[]'):
                permission_list.append(Permission.objects.get(id=permision_id))
            group,created = Group.objects.get_or_create(name = self.request.POST.get('group_name'))
            group.permissions.set(permission_list)
            group.save()
            return JsonResponse({"message":"Role Group Created SuccessFully"})
        except Exception as e:
            return JsonResponse({"message":e.args})

class GroupUpdateView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            permission_id = []
            for existing in Group.objects.get(id=self.kwargs['pk']).permissions.all():
                permission_id.append(existing.id)

            context = {'existing_permissions':Permission.objects.all().exclude(id__in=permission_id)} 
            context['groups'] = Group.objects.all()
            try:
                context['current_group'] = Group.objects.get(id=self.kwargs['pk'])   
            except Group.DoesNotExist:
                return redirect("admin:error_404")
            context['subtitle'] = "User Role Form"
            return render(self.request,"admin/accounts/group_form_update.html",context)
        except Exception as e:
            return render(self.request,"admin/widgets/500.html",{'message':"Hint: "+str(e)})
    
    def post(self,*args,**kwargs):
        permission_list = []
        for permision_id in self.request.POST.getlist('sel_perm_list[]'):
            permission_list.append(Permission.objects.get(id=permision_id))
        group  = Group.objects.get(id = self.kwargs['pk'])
        group.name = self.request.POST['group_name']
        group.permissions.remove()
        group.permissions.set(permission_list)
        group.save()
        return JsonResponse({"message":"User Group Updated SuccessFully"})


class UserDeleteView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            userprofile = UserAccount.objects.get(id=self.kwargs['pk'])
            userprofile.expired = True
            userprofile.last_updated_by=self.request.user
            userprofile.last_updated_date = timezone.now()
            userprofile.save()
            messages.success(self.request,"Successfully Deleted User")
            return redirect("admin:users_list")
        except Exception as e:
            context={"message":e}
            return render(self.request,"admin/widgets/500.html",context=context)

class GroupDeleteView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            group = Group.objects.get(id=self.kwargs['pk'])
            group.delete()
            messages.success(self.request,"User Group Deleted Successfully")
            return redirect("admin:group_list")
        except Group.DoesNotExist as e:
            return render(self.request,"admin/widgets/404.html",{'message':"Hint: "+str(e)})