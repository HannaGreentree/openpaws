from django.urls import path
from . import views

app_name = "shelters"

urlpatterns = [
    path("", views.shelter_list, name="list"),
    path("<int:pk>/", views.shelter_detail, name="detail"),
]
