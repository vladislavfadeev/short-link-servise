from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("apps.dashboard.urls")),
    path("", include("apps.home.urls")),
    path("", include("apps.authuser.urls")),
    path("", include("apps.cutter.urls", namespace="cutter_url")),
]
