from django.urls import path
from . import views

app_name = "cases"

urlpatterns = [
    path("", views.case_list, name="list"),
    path("<int:pk>/", views.case_detail, name="detail"),
]
