from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("shelters/", include("shelters.urls")),
    path("cases/", include("cases.urls")),
    path("payments/", include("payments.urls")),  
]