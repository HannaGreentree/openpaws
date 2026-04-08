from django.shortcuts import get_object_or_404, render

from .models import Shelter


def shelter_list(request):
    shelters = Shelter.objects.all()
    return render(request, "shelters/shelter_list.html", {"shelters": shelters})


def shelter_detail(request, pk):
    shelter = get_object_or_404(Shelter, pk=pk)
    cases = shelter.cases.all()

    return render(
        request,
        "shelters/shelter_detail.html",
        {
            "shelter": shelter,
            "cases": cases,
        },
    )