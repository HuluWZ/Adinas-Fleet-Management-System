from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),  
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),  
    
    path('dropdown/',views.GetAllDropdownView.as_view(),name="dropdown_list"),

    path('create/',views.VehicleCreateAPIView.as_view(),name="add_vehicle"),
    path('image/<int:id>/', views.VehicleImageCreateView.as_view(), name='vehicle_image'),  
]
