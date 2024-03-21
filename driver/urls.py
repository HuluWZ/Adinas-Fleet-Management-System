from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateDriveView.as_view(), name='create_driver'),
    path('update/<int:driver_id>/', views.UpdateDriveView.as_view(), name='update_driver'),
    path('all/', views.GetAllDrivesView.as_view(), name='get_all_drivers'),
    path('get/<int:driver_id>/', views.GetOneDriveView.as_view(), name='get_one_driver'),
    path('delete/<int:driver_id>/', views.DeleteDriveView.as_view(), name='delete_driver'),
    path('activate/<int:driver_id>/', views.ActivateDeactivateDriveView.as_view(), name='activate_deactivate_driver'),
   
    path('owner/create/', views.CreateOwnerView.as_view(), name='create_owner'),
    path('owner/update/<int:driver_id>/', views.UpdateOwnerView.as_view(), name='update_owner'),
    path('owner/all/', views.GetAllOwnerView.as_view(), name='get_all_owners'),
    path('owner/get/<int:driver_id>/', views.GetOneOwnerView.as_view(), name='get_one_owner'),
    path('owner/delete/<int:driver_id>/', views.DeleteOwnerView.as_view(), name='delete_owner'),
    path('owner/activate/<int:driver_id>/', views.ActivateDeactivateOwnerView.as_view(), name='activate_deactivate_owner'),

]
