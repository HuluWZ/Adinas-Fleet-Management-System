from django.urls import path
from .views import (
    UserLoginVerifyView,
    UserSignupView,
    UserLoginInitiateView,
    UserProfileAPIView,
    UserGetAPIView,
    UserViewAllAPIView,
    UserUpdateAPIView,
    AssignVehicleFromSMS,
)

urlpatterns = [
    path("login/", UserLoginInitiateView.as_view(), name="user_initiate"),
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("verify/", UserLoginVerifyView.as_view(), name="user_verify"),
    path("profile/", UserProfileAPIView.as_view(), name="user_profile"),
    path("all/", UserViewAllAPIView.as_view(), name="user_all"),
    path("update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("get/<int:pk>/", UserGetAPIView.as_view(), name="user_one"),
    path(
        "assign/verify/sms/<int:vehicle_request_id>/<str:plate_id>/",
        AssignVehicleFromSMS.as_view(),
        name="assign_vehicle_sms",
    ),
]
