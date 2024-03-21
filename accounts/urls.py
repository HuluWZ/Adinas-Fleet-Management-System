
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import  signup,send_otp, verify_otp ,create_vehicle_from_view,WebMyProfileView , GetMyVehicle ,CreateMessageView ,DeleteVehicleView,ActivateDeactivateVehicleView,UpdateVehicleView,UpdateVehicleImageView,RemoveVehicleImage

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('send/', send_otp, name='send_otp'),
    path('verify/', verify_otp, name='verify_otp'),
    path('vehicle/register/', create_vehicle_from_view, name='register_vehicle'),
    path('vehicle/my/', GetMyVehicle.as_view(), name='my_vehicle'),
    path('vehicle/<int:vehicle_id>/update/', UpdateVehicleView.as_view(), name='update_vehicle'),
    path('vehicle/<int:vehicle_id>/delete/', DeleteVehicleView.as_view(), name='delete_vehicle'),
    path('vehicle/<int:vehicle_id>/activate-deactivate/', ActivateDeactivateVehicleView.as_view(), name='activate_deactivate_vehicle'),
    path('vehicle/image/<int:vehicle_id>/update/', UpdateVehicleImageView.as_view(), name='update_vehicle_image'),
    path('vehicle/image/<int:image_id>/delete/', RemoveVehicleImage.as_view(), name='remove_vehicle_image'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', WebMyProfileView.as_view(), name='profile'),
    path('contact/',CreateMessageView.as_view(),name="contact_us")

]
