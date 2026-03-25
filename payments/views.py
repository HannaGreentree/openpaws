# payments/views.py
from decimal import Decimal, InvalidOperation

import stripe
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from shelters.models import Shelter
from cases.models import Case
from .models import Donation


def _get_amount(request, default="5"):
    amount_str = (request.POST.get("amount") or default).strip()
    try:
        amount = Decimal(amount_str)
    except (InvalidOperation, TypeError):
        amount = Decimal(default)

    if amount <= 0:
        amount = Decimal(default)

    return amount


def _mark_donation_paid_from_session(session_id):
    """
    Marks the matching Donation as paid after a successful Stripe checkout.
    Safe to call multiple times.
    """
    if not session_id:
        return None

    donation = Donation.objects.filter(stripe_session_id=session_id).first()
    if donation:
        donation.paid = True
        donation.save(update_fields=["paid"])
    return donation


def balance(request):
    platform_total = (
        Donation.objects.filter(
            paid=True,
            case__isnull=True,
            donation_type="PLATFORM",
        ).aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    allocated_total = (
        Case.objects.filter(approved_amount__isnull=False)
        .aggregate(total=Sum("approved_amount"))["total"]
        or Decimal("0")
    )

    available_balance = platform_total - allocated_total

    thank_you_total = (
        Donation.objects.filter(
            paid=True,
            donation_type="THANK_YOU",
        ).aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    return render(
        request,
        "payments/balance.html",
        {
            "platform_total": platform_total,
            "allocated_total": allocated_total,
            "available_balance": available_balance,
            "thank_you_total": thank_you_total,
        },
    )


# -----------------------
# PLATFORM DONATION FLOW
# -----------------------
def donate_platform(request):
    return render(request, "payments/donate_platform.html")


def donate_platform_checkout(request):
    if request.method != "POST":
        return redirect("payments:donate_platform")

    if not getattr(settings, "STRIPE_SECRET_KEY", ""):
        return HttpResponse("Stripe secret key not configured.", status=500)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    amount = _get_amount(request, default="10")

    success_url = (
        request.build_absolute_uri(reverse("payments:success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("payments:cancel"))

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": "Donate to OpenPaws platform balance"},
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"donation_type": "PLATFORM"},
    )

    Donation.objects.create(
        user=request.user if request.user.is_authenticated else None,
        donation_type="PLATFORM",
        amount=amount,
        stripe_session_id=session.id,
        paid=False,
    )

    return redirect(session.url, code=303)


# -----------------------
# THANK YOU FLOW (SHELTER)
# -----------------------
def thank_you(request, shelter_id):
    shelter = get_object_or_404(Shelter, pk=shelter_id)

    thank_you_balance = (
        Donation.objects.filter(
            paid=True,
            donation_type="THANK_YOU",
            shelter=shelter,
        ).aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    return render(
        request,
        "payments/thank_you.html",
        {
            "shelter": shelter,
            "thank_you_balance": thank_you_balance,
        },
    )


def thank_you_checkout(request, shelter_id):
    shelter = get_object_or_404(Shelter, pk=shelter_id)

    if request.method != "POST":
        return redirect("payments:thank_you", shelter_id=shelter.id)

    if not getattr(settings, "STRIPE_SECRET_KEY", ""):
        return HttpResponse("Stripe secret key not configured.", status=500)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    amount = _get_amount(request, default="5")

    success_url = (
        request.build_absolute_uri(reverse("payments:success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("payments:cancel"))

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": f"Thank You for {shelter.name}"},
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "donation_type": "THANK_YOU",
            "shelter_id": str(shelter.id),
        },
    )

    Donation.objects.create(
        user=request.user if request.user.is_authenticated else None,
        shelter=shelter,
        donation_type="THANK_YOU",
        amount=amount,
        stripe_session_id=session.id,
        paid=False,
    )

    return redirect(session.url, code=303)


def payment_success(request):
    session_id = request.GET.get("session_id")
    donation = None

    if session_id and getattr(settings, "STRIPE_SECRET_KEY", ""):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            session = stripe.checkout.Session.retrieve(session_id)

            if session.get("payment_status") == "paid":
                donation = _mark_donation_paid_from_session(session_id)

        except Exception:
            donation = Donation.objects.filter(stripe_session_id=session_id).first()

    return render(
        request,
        "payments/success.html",
        {
            "donation": donation,
        },
    )


def payment_cancel(request):
    return render(request, "payments/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    if not getattr(settings, "STRIPE_WEBHOOK_SECRET", ""):
        return HttpResponse(status=200)

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id")
        if session_id:
            _mark_donation_paid_from_session(session_id)

    return HttpResponse(status=200)