from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from ..models import Slider , Service ,Testimonal , Partner, About , Message
from ..forms import SliderForm , ServiceForm ,TestimonalForm , PartnerForm, AboutForm , MessageForm

class CreateMessageView(LoginRequiredMixin,View):
    def get(self, request):
        form = MessageForm()  
        context ={
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Add Message ",
            'page_title':"Add Message Form",
            'form':form
        }
        return render(request, 'admin/website/message/message_form.html', context=context)
    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Message Added successfully")
            return redirect("admin:get_all_message")
        else:
            context = {
              'form': form ,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Message ",
            }
            return render(request, 'admin/website/message/message_form.html', context=context)



class UpdateMessageView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Message, id=web_id)
        form = MessageForm(instance=client)  
        context = {
            'form': form ,
            'object':client,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Message Update",
        }
        return render(request, 'admin/website/message/message_detail.html', context=context)

    def post(self, request, web_id):
        client = get_object_or_404(Message, id=web_id)
        form = MessageForm(request.POST,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Message Updated successfully")
            return redirect("admin:get_all_message")
        else:
            context = {
              'form': form ,
              'object':client,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Message Update",
            }
            return render(request, 'admin/website/message/message_detail.html', context=context)



class GetAllMessageView(LoginRequiredMixin,View):
    def get(self, request):
        vehicles = Message.objects.all()
        context = {
            'vehicle_data': vehicles ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Message List",
        }
        return render(request,"admin/website/message/message_list.html",context=context)


class DeleteMessageView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Message, id=web_id)
        client.delete()
        messages.success(request,"Message Deleted successfully")
        return redirect("admin:get_all_message")
    

class CreateSliderView(LoginRequiredMixin,View):
    def get(self, request):
        form = SliderForm()  
        context ={
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Add Slider ",
            'page_title':"Add Slider Form",
            'form':form
        }
        return render(request, 'admin/website/slider/slider_form.html', context=context)
    def post(self, request):
        form = SliderForm(request.POST,request.FILES)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Slider Added successfully")
            return redirect("admin:get_all_slider")
        else:
            context = {
              'form': form ,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Slider ",
            }
            return render(request, 'admin/website/slider/slider_form.html', context=context)



class UpdateSliderView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Slider, id=web_id)
        form = SliderForm(instance=client)  # Create an instance of your form
        context = {
            'object':client,
            'form': form ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Slider Update",
        }
        return render(request, 'admin/website/slider/slider_detail.html', context=context)

    def post(self, request, web_id):
        client = get_object_or_404(Slider, id=web_id)
        form = SliderForm(request.POST,request.FILES,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Slider Updated successfully")
            return redirect("admin:get_all_slider")
        else:
            context = {
              'form': form ,
              'object':client,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Slider Update",
            }
            return render(request, 'admin/website/slider/slider_detail.html', context=context)



class GetAllSliderView(LoginRequiredMixin,View):
    def get(self, request):
        vehicles = Slider.objects.all()
        context = {
            'vehicle_data': vehicles ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Slider List",
        }
        return render(request,"admin/website/slider/slider_list.html",context=context)


class DeleteSliderView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Slider, id=web_id)
        client.delete()
        messages.success(request,"Slider Deleted successfully")
        return redirect("admin:get_all_slider")

class ActivateDeactivateSliderView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Slider, id=web_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Slider  {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_slider")   
      
class GetOneSliderView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Slider, id=web_id)
        form = SliderForm()  # Create an instance of your form
        context =  {
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Slider Detail",
            'page_title':"Update Slider Detail",
            'object':client,
            'form':form
        }
        return render(request,"admin/website/slider/slider_detail.html",context=context)

class CreateAboutView(LoginRequiredMixin,View):
    def get(self, request):
        form = AboutForm()  
        context ={
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Add About ",
            'page_title':"Add About Form",
            'form':form
        }
        return render(request, 'admin/website/about/about_form.html', context=context)
    def post(self, request):
        form = AboutForm(request.POST,request.FILES)
        if form.is_valid():
            client = form.save()
            messages.success(request,"About Added successfully")
            return redirect("admin:get_all_about")
        else:
            context = {
              'form': form ,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Slider ",
            }
            return render(request, 'admin/website/about/about_form.html', context=context)



class UpdateAboutView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(About, id=web_id)
        form = AboutForm(instance=client)  # Create an instance of your form
        context = {
            'object':client,
            'form': form ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"About Update",
        }
        return render(request, 'admin/website/about/about_detail.html', context=context)

    def post(self, request, web_id):
        client = get_object_or_404(About, id=web_id)
        form = AboutForm(request.POST,request.FILES,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"About Updated successfully")
            return redirect("admin:get_all_about")
        else:
            context = {
              'form': form ,
              'object':client,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"About Update",
            }
            return render(request, 'admin/website/about/about_detail.html', context=context)



class GetAllAboutView(LoginRequiredMixin,View):
    def get(self, request):
        vehicles = About.objects.all()
        context = {
            'vehicle_data': vehicles ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"About List",
        }
        return render(request,"admin/website/about/about_list.html",context=context)


class DeleteAboutView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(About, id=web_id)
        client.delete()
        messages.success(request,"About Deleted successfully")
        return redirect("admin:get_all_about")

class ActivateDeactivateAboutView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(About, id=web_id)
        client.is_active = not client.is_active
        client.save()
        message = f'About  {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_about")   
      
class GetOneAboutView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(About, id=web_id)
        form = AboutForm()  # Create an instance of your form
        context =  {
            'web':'active',
            'web_submenu':'active',
            'subtitle':"About Detail",
            'page_title':"Update About Detail",
            'object':client,
            'form':form
        }
        return render(request,"admin/website/about/about_detail.html",context=context)


class CreateServiceView(LoginRequiredMixin,View):
    def get(self, request):
        form = AboutForm()  
        context ={
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Add Service ",
            'page_title':"Add Service Form",
            'form':form
        }
        return render(request, 'admin/website/service/service_form.html', context=context)
    def post(self, request):
        form = ServiceForm(request.POST,request.FILES)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Service Added successfully")
            return redirect("admin:get_all_service")
        else:
            context = {
              'form': form ,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Slider ",
            }
            return render(request, 'admin/website/service/service_form.html', context=context)



class UpdateServiceView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Service, id=web_id)
        form = ServiceForm(instance=client)  # Create an instance of your form
        context = {
            'object':client,
            'form': form ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Service Update",
        }
        return render(request, 'admin/website/service/service_detail.html', context=context)

    def post(self, request, web_id):
        client = get_object_or_404(Service, id=web_id)
        form = ServiceForm(request.POST,request.FILES,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Service Updated successfully")
            return redirect("admin:get_all_service")
        else:
            context = {
              'form': form ,
              'object':client,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Service Update",
            }
            return render(request, 'admin/website/service/service_detail.html', context=context)



class GetAllServiceView(LoginRequiredMixin,View):
    def get(self, request):
        vehicles = Service.objects.all()
        context = {
            'vehicle_data': vehicles ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Service List",
        }
        return render(request,"admin/website/service/service_list.html",context=context)


class DeleteServiceView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Service, id=web_id)
        client.delete()
        messages.success(request,"Service Deleted successfully")
        return redirect("admin:get_all_service")

class ActivateDeactivateServiceView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Service, id=web_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Service  {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_service")   
      
class GetOneServiceView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Service, id=web_id)
        form = ServiceForm()  # Create an instance of your form
        context =  {
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Service Detail",
            'page_title':"Update Service Detail",
            'object':client,
            'form':form
        }
        return render(request,"admin/website/service/service_detail.html",context=context)


class CreateTestimonalView(LoginRequiredMixin,View):
    def get(self, request):
        form = TestimonalForm()  
        context ={
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Add Testimonial ",
            'page_title':"Add Testimonial Form",
            'form':form
        }
        return render(request, 'admin/website/testimonal/testimonial_form.html', context=context)
    def post(self, request):
        form = TestimonalForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Testimonal Added successfully")
            return redirect("admin:get_all_testimonal")
        else:
            context = {
              'form': form ,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Testimonial ",
            }
            return render(request, 'admin/website/testimonal/testimonial_form.html', context=context)



class UpdateTestimonalView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Testimonal, id=web_id)
        form = TestimonalForm(instance=client)  # Create an instance of your form
        context = {
            'object':client,
            'form': form ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Testimonial Update",
        }
        return render(request, 'admin/website/testimonal/testimonial_detail.html', context=context)

    def post(self, request, web_id):
        client = get_object_or_404(Testimonal, id=web_id)
        form = TestimonalForm(request.POST,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Testimonal Updated successfully")
            return redirect("admin:get_all_testimonal")
        else:
            context = {
              'form': form ,
              'object':client,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Testimonal Update",
            }
            return render(request, 'admin/website/testimonal/testimonial_detail.html', context=context)



class GetAllTestimonalView(LoginRequiredMixin,View):
    def get(self, request):
        vehicles = Testimonal.objects.all()
        context = {
            'vehicle_data': vehicles ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Testimonal List",
        }
        return render(request,"admin/website/testimonal/testimonial_list.html",context=context)


class DeleteTestimonalView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Testimonal, id=web_id)
        client.delete()
        messages.success(request,"Testimonal Deleted successfully")
        return redirect("admin:get_all_testimonal")

class ActivateDeactivateTestimonalView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Testimonal, id=web_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Testimonal  {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_testimonal")   
      
class GetOneTestimonalView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Testimonal, id=web_id)
        form = TestimonalForm()  # Create an instance of your form
        context =  {
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Testimonal Detail",
            'page_title':"Update Testimonal Detail",
            'object':client,
            'form':form
        }
        return render(request,"admin/website/testimonal/testimonial_detail.html",context=context)


class CreatePartnerView(LoginRequiredMixin,View):
    def get(self, request):
        form = PartnerForm()  
        context ={
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Add Partner ",
            'page_title':"Add Partner Form",
            'form':form
        }
        return render(request, 'admin/website/partner/partner_form.html', context=context)
    def post(self, request):
        form = PartnerForm(request.POST,request.FILES)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Partner Added successfully")
            return redirect("admin:get_all_partner")
        else:
            context = {
              'form': form ,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Slider ",
            }
            return render(request, 'admin/website/partner/partner_form.html', context=context)



class UpdatePartnerView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Partner, id=web_id)
        form = PartnerForm(instance=client)  # Create an instance of your form
        context = {
            'object':client,
            'form': form ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Partner Update",
        }
        return render(request, 'admin/website/partner/partner_detail.html', context=context)

    def post(self, request, web_id):
        client = get_object_or_404(Partner, id=web_id)
        form = PartnerForm(request.POST,request.FILES,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Partner Updated successfully")
            return redirect("admin:get_all_partner")
        else:
            context = {
              'form': form ,
              'object':client,
              'web':'active',
              'web_submenu':'active',
              'subtitle':"Partner Update",
            }
            return render(request, 'admin/website/partner/partner_detail.html', context=context)



class GetAllPartnerView(LoginRequiredMixin,View):
    def get(self, request):
        vehicles = Partner.objects.all()
        context = {
            'vehicle_data': vehicles ,
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Partner List",
        }
        return render(request,"admin/website/partner/partner_list.html",context=context)


class DeletePartnerView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Partner, id=web_id)
        client.delete()
        messages.success(request,"Partner Deleted successfully")
        return redirect("admin:get_all_partner")

class ActivateDeactivatePartnerView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Partner, id=web_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Partner  {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_partner")   
      
class GetOnePartnerView(LoginRequiredMixin,View):
    def get(self, request, web_id):
        client = get_object_or_404(Partner, id=web_id)
        form = PartnerForm()  # Create an instance of your form
        context =  {
            'web':'active',
            'web_submenu':'active',
            'subtitle':"Partner Detail",
            'page_title':"Update Partner Detail",
            'object':client,
            'form':form
        }
        return render(request,"admin/website/partner/partner_detail.html",context=context)
