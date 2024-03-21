from django.contrib import admin
from functools import update_wrapper
from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from accounts.forms import AdminLoginForm
from core.views import *
from accounts.views import *
from client.views import *
from web.views.admin import *
from driver.views import *
from vehicle.views import *
from booking.views import *

class AFMSAdminSite(admin.AdminSite):
    login_form = AdminLoginForm

    def get_urls(self):
        urls = super().get_urls()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        my_urls = [
            path("", wrap(IndexView.as_view()), name="index"),
            path(
                "delete-user/<pk>/", wrap(UserDeleteView.as_view()), name="delete_user"
            ),
            path("notification/<pk>/<int:vehicle_id>/",wrap(MarkNotificationSeenView.as_view()),name="notification_seen"),
            path(
                "create-my-staff/",
                wrap(CreateCompanyStaff.as_view()),
                name="create_my_staff",
            ),
            path("users_list/", wrap(UserListView.as_view()), name="users_list"),
            path(
                "suspend_user/<pk>/<option>/",
                wrap(SuspendUser.as_view()),
                name="suspend_user",
            ),
            path(
                "change-user-password/<pk>/",
                wrap(ChangeUserPassword.as_view()),
                name="change_user_password",
            ),
            path(
                "user_detail/<pk>/", wrap(UserDetailView.as_view()), name="user_detail"
            ),
            path(
                "update_my_profile/<pk>/",
                wrap(MyProfileView.as_view()),
                name="my_profile",
            ),
            path("group_list/", wrap(GroupList.as_view()), name="group_list"),
            path("manage_group/", wrap(GroupView.as_view()), name="create_group"),
            path(
                "group-update-view/<pk>/",
                wrap(GroupUpdateView.as_view()),
                name="update_group",
            ),
            path(
                "group-delete-view/<pk>/",
                wrap(GroupDeleteView.as_view()),
                name="delete_group",
            ),
            path("core/archives/", wrap(ArchiveList.as_view()), name="archives_list"),
            path(
                "core/archives-detail/<archive_type>/",
                wrap(ArchiveDetail.as_view()),
                name="archives_detail",
            ),
            path(
                "core/archives-remove-data/<id>/<archive_type>/",
                wrap(RemoveAll.as_view()),
                name="archives_remove",
            ),
            path(
                "core/archives-restore-back/<id>/<archive_type>/",
                wrap(RestoreArchive.as_view()),
                name="archives_restore",
            ),
            # Client
            path(
                "client/create/", wrap(CreateClientView.as_view()), name="create_client"
            ),
            path(
                "client/<int:client_id>/update/",
                wrap(UpdateClientView.as_view()),
                name="update_client",
            ),
            path(
                "recycle/client/all/", wrap(GetAllExpiredClientView.as_view()), name="recycle_all_clients"
            ),

            path(
                "client/all/", wrap(GetAllClientsView.as_view()), name="get_all_clients"
            ),
            path(
                "client/<int:client_id>/",
                wrap(GetOneClientView.as_view()),
                name="get_one_client",
            ),
            path(
                "recycle/client/<int:client_id>/",
                wrap(ExpireClientView.as_view()),
                name="recycle_client",
            ),

            path(
                "client/<int:client_id>/delete/",
                wrap(DeleteClientView.as_view()),
                name="delete_client",
            ),
            path(
                "client/<int:client_id>/activate-deactivate/",
                wrap(ActivateDeactivateClientView.as_view()),
                name="activate_deactivate_client",
            ),
            # Content
            path(
                "content/about/create/",
                wrap(CreateAboutView.as_view()),
                name="create_about",
            ),
            path(
                "content/about/<int:web_id>/update/",
                wrap(UpdateAboutView.as_view()),
                name="update_about",
            ),
            path(
                "content/about/all/",
                wrap(GetAllAboutView.as_view()),
                name="get_all_about",
            ),
            path(
                "content/about/<int:web_id>/",
                wrap(GetOneAboutView.as_view()),
                name="get_one_about",
            ),
            path(
                "content/about/<int:web_id>/delete/",
                wrap(DeleteAboutView.as_view()),
                name="delete_about",
            ),
            path(
                "content/about/<int:web_id>/activate-deactivate/",
                wrap(ActivateDeactivateAboutView.as_view()),
                name="activate_deactivate_about",
            ),
            path(
                "content/partner/create/",
                wrap(CreatePartnerView.as_view()),
                name="create_partner",
            ),
            path(
                "content/partner/<int:web_id>/update/",
                wrap(UpdatePartnerView.as_view()),
                name="update_partner",
            ),
            path(
                "content/partner/all/",
                wrap(GetAllPartnerView.as_view()),
                name="get_all_partner",
            ),
            path(
                "content/partner/<int:web_id>/",
                wrap(GetOnePartnerView.as_view()),
                name="get_one_partner",
            ),
            path(
                "content/partner/<int:web_id>/delete/",
                wrap(DeletePartnerView.as_view()),
                name="delete_partner",
            ),
            path(
                "content/partner/<int:web_id>/activate-deactivate/",
                wrap(ActivateDeactivatePartnerView.as_view()),
                name="activate_deactivate_partner",
            ),
            path(
                "content/service/create/",
                wrap(CreateServiceView.as_view()),
                name="create_service",
            ),
            path(
                "content/service/<int:web_id>/update/",
                wrap(UpdateServiceView.as_view()),
                name="update_service",
            ),
            path(
                "content/service/all/",
                wrap(GetAllServiceView.as_view()),
                name="get_all_service",
            ),
            path(
                "content/service/<int:web_id>/",
                wrap(GetOneServiceView.as_view()),
                name="get_one_service",
            ),
            path(
                "content/service/<int:web_id>/delete/",
                wrap(DeleteServiceView.as_view()),
                name="delete_service",
            ),
            path(
                "content/service/<int:web_id>/activate-deactivate/",
                wrap(ActivateDeactivateServiceView.as_view()),
                name="activate_deactivate_service",
            ),
            path(
                "content/slider/create/",
                wrap(CreateSliderView.as_view()),
                name="create_slider",
            ),
            path(
                "content/slider/<int:web_id>/update/",
                wrap(UpdateSliderView.as_view()),
                name="update_slider",
            ),
            path(
                "content/slider/all/",
                wrap(GetAllSliderView.as_view()),
                name="get_all_slider",
            ),
            path(
                "content/slider/<int:web_id>/",
                wrap(GetOneSliderView.as_view()),
                name="get_one_slider",
            ),
            path(
                "content/slider/<int:web_id>/delete/",
                wrap(DeleteSliderView.as_view()),
                name="delete_slider",
            ),
            path(
                "content/slider/<int:web_id>/activate-deactivate/",
                wrap(ActivateDeactivateSliderView.as_view()),
                name="activate_deactivate_slider",
            ),
            path(
                "content/message/create/",
                wrap(CreateMessageView.as_view()),
                name="create_message",
            ),
            path(
                "content/message/<int:web_id>/update/",
                wrap(UpdateMessageView.as_view()),
                name="update_message",
            ),
            path(
                "content/message/all/",
                wrap(GetAllMessageView.as_view()),
                name="get_all_message",
            ),
            path(
                "content/message/<int:web_id>/delete/",
                wrap(DeleteMessageView.as_view()),
                name="delete_message",
            ),
            path(
                "content/testimonal/create/",
                wrap(CreateTestimonalView.as_view()),
                name="create_testimonal",
            ),
            path(
                "content/testimonal/<int:web_id>/update/",
                wrap(UpdateTestimonalView.as_view()),
                name="update_testimonal",
            ),
            path(
                "content/testimonal/all/",
                wrap(GetAllTestimonalView.as_view()),
                name="get_all_testimonal",
            ),
            path(
                "content/testimonal/<int:web_id>/",
                wrap(GetOneTestimonalView.as_view()),
                name="get_one_testimonal",
            ),
            path(
                "content/testimonal/<int:web_id>/delete/",
                wrap(DeleteTestimonalView.as_view()),
                name="delete_testimonal",
            ),
            path(
                "content/testimonal/<int:web_id>/activate-deactivate/",
                wrap(ActivateDeactivateTestimonalView.as_view()),
                name="activate_deactivate_testimonal",
            ),
            #   Driver
            path(
                "driver/create/", wrap(CreateDriveView.as_view()), name="create_driver"
            ),
            path(
                "driver/update/<int:driver_id>/",
                wrap(UpdateDriveView.as_view()),
                name="update_driver",
            ),
            path(
                "driver/all/", wrap(GetAllDrivesView.as_view()), name="get_all_drivers"
            ),
            path(
                "recycle/driver/all/", wrap(GetAllExpiredDrivesView.as_view()), name="recycle_all_drivers"
            ),
            path(
                "driver/get/<int:driver_id>/",
                wrap(GetOneDriveView.as_view()),
                name="get_one_driver",
            ),
            path(
                "recycle/driver/<int:driver_id>/",
                wrap(ExpireDriverView.as_view()),
                name="recycle_driver",
            ),

            path(
                "driver/delete/<int:driver_id>/",
                wrap(DeleteDriveView.as_view()),
                name="delete_driver",
            ),
            path(
                "driver/activate/<int:driver_id>/",
                wrap(ActivateDeactivateDriveView.as_view()),
                name="activate_deactivate_driver",
            ),
            # Owner
            path(
                "owner/create/", wrap(CreateOwnerView.as_view()), name="create_owner"
            ),
            path(
                "owner/update/<int:driver_id>/",
                wrap(UpdateOwnerView.as_view()),
                name="update_owner",
            ),
            path(
                "owner/all/", wrap(GetAllOwnerView.as_view()), name="get_all_owners"
            ),
            path(
                "recycle/owner/all/", wrap(GetAllExpiredOwnerView.as_view()), name="recycle_all_owners"
            ),
            path(
                "owner/get/<int:driver_id>/",
                wrap(GetOneOwnerView.as_view()),
                name="get_one_owner",
            ),
            path(
                "recycle/owner/<int:driver_id>/",
                wrap(ExpireOwnerView.as_view()),
                name="recycle_owner",
            ),

            path(
                "owner/delete/<int:driver_id>/",
                wrap(DeleteOwnerView.as_view()),
                name="delete_owner",
            ),
            path(
                "owner/activate/<int:driver_id>/",
                wrap(ActivateDeactivateOwnerView.as_view()),
                name="activate_deactivate_owner",
            ),

            #   Vehicle
            path(
                "vehicle/create/",
                wrap(CreateVehicleView.as_view()),
                name="create_vehicle",
            ),
            path(
                "vehicle/<int:vehicle_id>/update/",
                wrap(UpdateVehicleView.as_view()),
                name="update_vehicle",
            ),
             path(
                "vehicle/image/<int:vehicle_id>/update/",
                wrap(UpdateVehicleImageView.as_view()),
                name="update_vehicle_image",
            ),
             path(
                "vehicle/image/<int:image_id>/",
                wrap(RemoveVehicleImage.as_view()),
                name="remove_vehicle_image",
            ),
            path(
                "vehicle/all/",
                wrap(GetAllVehiclesView.as_view()),
                name="get_all_vehicles",
            ),
            path(
                "recycle/vehicle/all/", wrap(GetAllExpiredVehicleView.as_view()), name="recycle_all_vehicles"
            ),

            path(
                "vehicle/<int:vehicle_id>/",
                wrap(GetOneVehicleView.as_view()),
                name="get_one_vehicle",
            ),
            path(
                "recycle/vehicle/<int:vehicle_id>/",
                wrap(ExpireVehicleView.as_view()),
                name="recycle_vehicle",
            ),

            path(
                "vehicle/<int:vehicle_id>/delete/",
                wrap(DeleteVehicleView.as_view()),
                name="delete_vehicle",
            ),
            path(
                "vehicle/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateVehicleView.as_view()),
                name="activate_deactivate_vehicle",
            ),
            path(
                "vehicle/interest/create/",
                wrap(CreateInterestView.as_view()),
                name="create_interest",
            ),
            path(
                "vehicle/type/<int:vehicle_id>/update/",
                wrap(UpdateInterestView.as_view()),
                name="update_interest",
            ),
            path(
                "vehicle/interest/all/", wrap(GetAllInterestView.as_view()), name="get_all_interest"
            ),
            path(
                "report/vehicle/", wrap(FilterVehicleView.as_view()), name="get_all_filter_vehicle"
            ),
            path(
                "report/booking/", wrap(FilterVehicleRequestView.as_view()), name="get_all_filter_booking"
            ),
            path(
                "vehicle/interest/<int:vehicle_id>/delete/",
                wrap(DeleteInterestView.as_view()),
                name="delete_interest",
            ),
            path(
                "vehicle/interest/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateInterestView.as_view()),
                name="activate_deactivate_interest",
            ),

            path(
                "vehicle/type/create/",
                wrap(CreateTypeView.as_view()),
                name="create_type",
            ),
            path(
                "vehicle/type/<int:vehicle_id>/update/",
                wrap(UpdateTypeView.as_view()),
                name="update_type",
            ),
            path(
                "vehicle/type/all/", wrap(GetAllTypeView.as_view()), name="get_all_type"
            ),
            path(
                "vehicle/type/<int:vehicle_id>/",
                wrap(GetOneTypeView.as_view()),
                name="get_one_type",
            ),
            path(
                "vehicle/type/<int:vehicle_id>/delete/",
                wrap(DeleteTypeView.as_view()),
                name="delete_type",
            ),
            path(
                "vehicle/type/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateTypeView.as_view()),
                name="activate_deactivate_type",
            ),
            path(
                "vehicle/model/create/",
                wrap(CreateModelView.as_view()),
                name="create_model",
            ),
            path(
                "vehicle/model/<int:vehicle_id>/update/",
                wrap(UpdateModelView.as_view()),
                name="update_model",
            ),
            path(
                "vehicle/model/all/",
                wrap(GetAllModelView.as_view()),
                name="get_all_model",
            ),
            path(
                "vehicle/model/<int:vehicle_id>/",
                wrap(GetOneModelView.as_view()),
                name="get_one_model",
            ),
            path(
                "vehicle/model/<int:vehicle_id>/delete/",
                wrap(DeleteModelView.as_view()),
                name="delete_model",
            ),
            path(
                "vehicle/model/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateModelView.as_view()),
                name="activate_deactivate_model",
            ),
            path(
                "vehicle/brand/create/",
                wrap(CreateBrandView.as_view()),
                name="create_brand",
            ),
            path(
                "vehicle/brand/<int:vehicle_id>/update/",
                wrap(UpdateBrandView.as_view()),
                name="update_brand",
            ),
            path(
                "vehicle/brand/all/",
                wrap(GetAllBrandView.as_view()),
                name="get_all_brand",
            ),
            path(
                "vehicle/brand/<int:vehicle_id>/",
                wrap(GetOneBrandView.as_view()),
                name="get_one_brand",
            ),
            path(
                "vehicle/brand/<int:vehicle_id>/delete/",
                wrap(DeleteBrandView.as_view()),
                name="delete_brand",
            ),
            path(
                "vehicle/brand/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateBrandView.as_view()),
                name="activate_deactivate_brand",
            ),
            path(
                "vehicle/color/create/",
                wrap(CreateColorView.as_view()),
                name="create_color",
            ),
            path(
                "vehicle/color/<int:vehicle_id>/update/",
                wrap(UpdateColorView.as_view()),
                name="update_color",
            ),
            path(
                "vehicle/color/all/",
                wrap(GetAllColorView.as_view()),
                name="get_all_color",
            ),
            path(
                "vehicle/color/<int:vehicle_id>/",
                wrap(GetOneColorView.as_view()),
                name="get_one_color",
            ),
            path(
                "vehicle/color/<int:vehicle_id>/delete/",
                wrap(DeleteColorView.as_view()),
                name="delete_color",
            ),
            path(
                "vehicle/color/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateColorView.as_view()),
                name="activate_deactivate_color",
            ),
            path(
                "vehicle/request/create/",
                wrap(CreateVehicleRequestView.as_view()),
                name="create_request",
            ),
            path(
                "vehicle/request/<int:vehicle_id>/update/",
                wrap(UpdateVehicleRequestView.as_view()),
                name="update_request",
            ),

            path(
                "vehicle/request/assign/<int:vehicle_id>/",
                wrap(AssignVehicleToVehicleRequestView.as_view()),
                name="assign_request",
            ),
            path(
                "vehicle/request/assign/sms/<int:vehicle_id>/",
                wrap(SendSMSforVehicleRequestView.as_view()),
                name="assign_request_sms",
            ),
            path(
                "vehicle/request/assign/inapp/<int:vehicle_id>/",
                wrap(SendInAppforVehicleRequest.as_view()),
                name="send_inapp_message",
            ),
            path(
                "vehicle/request/assign/send-telegram/<int:vehicle_id>/",
                wrap(SendTelegramforVehicleRequestView.as_view()),
                name="send_telegram",
            ),
            path(
                "vehicle/request/assign/remove/<int:vehicle_id>/<int:v_id>/",
                wrap(RemoveAssignVehicleToVehicleRequestView.as_view()),
                name="remove_assigned_request",
            ),
            path(
                "recycle/vehicle/request/all/", wrap(GetAllExpiredVehicleRequestView.as_view()), name="recycle_all_request"
            ),

            path(
                "vehicle/request/all/",
                wrap(GetAllVehicleRequestView.as_view()),
                name="get_all_request",
            ),
            path(
                "vehicle/request/<int:vehicle_id>/",
                wrap(GetOneVehicleRequestView.as_view()),
                name="get_one_request",
            ),
            path(
                "recycle/vehicle/request/<int:vehicle_id>/",
                wrap(ExpireVehicleRequestView.as_view()),
                name="recycle_request",
            ),

            path(
                "vehicle/request/<int:vehicle_id>/delete/",
                wrap(DeleteVehicleRequestView.as_view()),
                name="delete_request",
            ),
            path(
                "vehicle/request/<int:vehicle_id>/activate-deactivate/",
                wrap(ActivateDeactivateVehicleRequestView.as_view()),
                name="activate_deactivate_request",
            ),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        return my_urls + urls


admin_site = AFMSAdminSite(name="afmsadmin")
