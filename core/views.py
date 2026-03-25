from django.shortcuts import render
from shelters.models import Shelter


def home(request):
    shelters = Shelter.objects.all().order_by("name")
    return render(request, "core/home.html", {
        "shelters": shelters
    })