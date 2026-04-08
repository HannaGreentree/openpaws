from django.shortcuts import render, get_object_or_404
from django.db.models import Sum

from .models import Shelter
from payments.models import Donation
from cases.models import Case


def shelter_list(request):
    shelters = Shelter.objects.all()
    return render(request, "shelters/shelter_list.html", {"shelters": shelters})


def shelter_detail(request, pk):
    shelter = get_object_or_404(Shelter, pk=pk)

    thank_you_balance = (
        Donation.objects.filter(
            shelter=shelter,
            paid=True,
            donation_type="THANK_YOU",
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    cases = Case.objects.filter(shelter=shelter)

    context = {
        "shelter": shelter,
        "cases": cases,
        "thank_you_balance": thank_you_balance,
    }

    return render(request, "shelters/shelter_detail.html", context)