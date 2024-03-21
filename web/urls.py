from django.urls import path
from .views import admin

urlpatterns = [
    path('about/create/', admin.CreateAboutView.as_view(), name='create_about'),
    path('about/<int:web_id>/update/', admin.UpdateAboutView.as_view(), name='update_about'),
    path('about/all/', admin.GetAllAboutView.as_view(), name='get_all_about'),
    path('about/<int:web_id>/', admin.GetOneAboutView.as_view(), name='get_one_about'),
    path('about/<int:web_id>/delete/', admin.DeleteAboutView.as_view(), name='delete_about'),
    path('about/<int:web_id>/activate-deactivate/', admin.ActivateDeactivateAboutView.as_view(), name='activate_deactivate_about'),

    path('partner/create/', admin.CreatePartnerView.as_view(), name='create_partner'),
    path('partner/<int:web_id>/update/', admin.UpdatePartnerView.as_view(), name='update_partner'),
    path('partner/all/', admin.GetAllPartnerView.as_view(), name='get_all_partner'),
    path('partner/<int:web_id>/', admin.GetOnePartnerView.as_view(), name='get_one_partner'),
    path('partner/<int:web_id>/delete/', admin.DeletePartnerView.as_view(), name='delete_partner'),
    path('partner/<int:web_id>/activate-deactivate/', admin.ActivateDeactivatePartnerView.as_view(), name='activate_deactivate_partner'),

    path('service/create/', admin.CreateServiceView.as_view(), name='create_service'),
    path('service/<int:web_id>/update/', admin.UpdateServiceView.as_view(), name='update_service'),
    path('service/all/', admin.GetAllServiceView.as_view(), name='get_all_service'),
    path('service/<int:web_id>/', admin.GetOneServiceView.as_view(), name='get_one_service'),
    path('service/<int:web_id>/delete/', admin.DeleteServiceView.as_view(), name='delete_service'),
    path('service/<int:web_id>/activate-deactivate/', admin.ActivateDeactivateServiceView.as_view(), name='activate_deactivate_service'),

    path('slider/create/', admin.CreateSliderView.as_view(), name='create_slider'),
    path('slider/<int:web_id>/update/', admin.UpdateSliderView.as_view(), name='update_slider'),
    path('slider/all/', admin.GetAllSliderView.as_view(), name='get_all_slider'),
    path('slider/<int:web_id>/', admin.GetOneSliderView.as_view(), name='get_one_slider'),
    path('slider/<int:web_id>/delete/', admin.DeleteSliderView.as_view(), name='delete_slider'),
    path('slider/<int:web_id>/activate-deactivate/', admin.ActivateDeactivateSliderView.as_view(), name='activate_deactivate_slider'),

    path('testimonal/create/', admin.CreateTestimonalView.as_view(), name='create_testimonal'),
    path('testimonal/<int:web_id>/update/', admin.UpdateTestimonalView.as_view(), name='update_testimonal'),
    path('testimonal/all/', admin.GetAllTestimonalView.as_view(), name='get_all_testimonal'),
    path('testimonal/<int:web_id>/', admin.GetOneTestimonalView.as_view(), name='get_one_testimonal'),
    path('testimonal/<int:web_id>/delete/', admin.DeleteTestimonalView.as_view(), name='delete_testimonal'),
    path('testimonal/<int:web_id>/activate-deactivate/', admin.ActivateDeactivateTestimonalView.as_view(), name='activate_deactivate_testimonal'),
  
]
