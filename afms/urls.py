"""
URL configuration for AFM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from web.views.front import WebIndexView

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

router = DefaultRouter()

router.register("devices", FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path(
        "firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="firebase-messaging-sw.js",
            content_type="application/javascript",
        ),
        name="firebase-messaging-sw.js",
    ),
     path(
        "login",
        TemplateView.as_view(
            template_name="website/login.html",
        ),
    ),
    path("", WebIndexView.as_view(), name="web_index"),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.api.urls")),
    path("api/vehicle/", include("vehicle.api.urls")),
    path("api/owner/", include("driver.api.urls")),
    path("account/",include("accounts.urls")),
    path("vehicle/",include("vehicle.urls")),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
