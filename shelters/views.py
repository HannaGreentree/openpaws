from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404

from .models import Shelter
from payments.models import Donation


def shelter_list(request):
    shelters = Shelter.objects.all().order_by("name")
    return render(request, "shelters/shelter_list.html", {"shelters": shelters})


def shelter_detail(request, pk):
    shelter = get_object_or_404(Shelter, pk=pk)

    Case = shelter.case_set.model
    cases = Case.objects.filter(shelter=shelter).order_by("-created_at")

    thank_you_balance = (
        Donation.objects.filter(
            paid=True,
            donation_type="THANK_YOU",
            shelter=shelter,
        ).aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    return render(
        request,
        "shelters/shelter_detail.html",
        {
            "shelter": shelter,
            "cases": cases,
            "thank_you_balance": thank_you_balance,
        },
    )