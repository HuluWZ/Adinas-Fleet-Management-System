from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Client
from .forms import ClientForm 

class CreateClientView(LoginRequiredMixin,View):
    def get(self, request):
        form = ClientForm()  # Create an instance of your form
        context ={
            'clients':'active',
            'clients_submenu':'active',
            'subtitle':"Add Client",
            'page_title':"Add Client Form",
            'form':form
        }
        return render(request, 'admin/client/client_form.html', context=context)
    def post(self, request):
        form = ClientForm(request.POST,request.FILES)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Client Added successfully")
            return redirect("admin:get_all_clients")
        else:
            context ={
            'clients':'active',
            'clients_submenu':'active',
            'subtitle':"Add Client",
            'page_title':"Add Client Form",
            'form':form
           }
            return render(request, 'admin/client/client_form.html', context=context)

class UpdateClientView(LoginRequiredMixin,View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm(instance=client)  # Create an instance of your form
        context = {
            'form': form ,
            'object':client,
            'clients':'active',
            'clients_submenu':'active',
            'subtitle':"Clients Update",
        }
        return render(request, 'admin/client/client_detail.html', context=context)

    def post(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm(request.POST, request.FILES,instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request,"Client Updated successfully")
            return redirect("admin:get_all_clients")
        else:
           context = {
            'form': form ,
            'object':client,
            'clients':'active',
            'clients_submenu':'active',
            'subtitle':"Clients Update",
            }
        return render(request, 'admin/client/client_detail.html', context=context)



class GetAllClientsView(LoginRequiredMixin,View):
    def get(self, request):
        clients = Client.objects.filter(is_expired=False)
        context = {
            'clients_data': clients ,
            'clients':'active',
            'clients_submenu':'active',
            'subtitle':"Clients List",
        }
        return render(request,"admin/client/client_list.html",context=context)

class GetAllExpiredClientView(LoginRequiredMixin,View):
    def get(self, request):
        drives = Client.objects.filter(is_expired=True)
        context = {
            'clients_data': drives ,
            'archive':'active',
            'archive_submenu':'active',
            'subtitle':"Expired Clients List",
        }
        return render(request,"admin/recycle/client_list.html",context=context)

class GetOneClientView(LoginRequiredMixin,View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm()  # Create an instance of your form
        context =  {
            'clients':'active',
            'clients_submenu':'active',
            'subtitle':"Client Detail",
            'page_title':"Update Client Detail",
            'object':client,
            'form':form
        }
        return render(request,"admin/client/client_detail.html",context=context)

class DeleteClientView(LoginRequiredMixin,View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        messages.success(request,"Client Deleted successfully")
        return redirect("admin:get_all_clients")

class ExpireClientView(LoginRequiredMixin,View):
    def get(self, request, client_id):
        drive = get_object_or_404(Client, id=client_id)
        drive.is_expired = not drive.is_expired
        drive.save()
        message = f'Client {"Removed" if drive.is_expired else "Restored"} successfully'
        messages.success(request, message)
        url = "admin:recycle_all_clients" if not drive.is_expired else "admin:get_all_clients"
        return redirect(url)
   
class ActivateDeactivateClientView(LoginRequiredMixin,View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        client.is_active = not client.is_active
        client.save()
        message = f'Client {"Activated" if client.is_active else "Deactivated"} successfully'
        messages.success(request, message)
        return redirect("admin:get_all_clients")   
