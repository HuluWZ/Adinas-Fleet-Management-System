from django.urls import path
from . import views

urlpatterns = [
    path('owners/', views.OwnerListCreateAPIView.as_view(), name='owner_create'),
    path('owners/<int:pk>/', views.OwnerListDetailView.as_view(), name='owner_detail'),
    path('drivers/', views.DriverListCreateAPIView.as_view(), name='driver_create'),
    path('drivers/<int:pk>/', views.DriverListDetailView.as_view(), name='driver_detail')

]
