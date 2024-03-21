from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateClientView.as_view(), name='create_client'),
    path('<int:client_id>/update/', views.UpdateClientView.as_view(), name='update_client'),
    path('all/', views.GetAllClientsView.as_view(), name='get_all_clients'),
    path('<int:client_id>/', views.GetOneClientView.as_view(), name='get_one_client'),
    path('<int:client_id>/delete/', views.DeleteClientView.as_view(), name='delete_client'),
    path('<int:client_id>/activate-deactivate/', views.ActivateDeactivateClientView.as_view(), name='activate_deactivate_client'),
]
