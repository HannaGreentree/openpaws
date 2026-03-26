from decimal import Decimal
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .models import Case
from payments.models import Donation


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "shelter",
        "status",
        "amount_requested",
        "amount_funded",
        "approved_amount",
    )
    list_filter = ("status", "shelter")
    search_fields = ("title", "shelter__name")

    def get_readonly_fields(self, request, obj=None):
        """
        Only superusers/admins should control approval fields in admin.
        Shelter users should not use admin for workflow actions.
        """
        ro = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            ro += ["approved_amount", "status", "processing_started_at", "proof_due_at"]
        return ro

    def save_model(self, request, obj, form, change):
        """
        When admin changes approved_amount, ensure platform balance is enough.
        Also record which admin approved the case.
        """
        if request.user.is_superuser:
            new_approved = obj.approved_amount or Decimal("0")

            old_approved = Decimal("0")
            if change and obj.pk:
                old_obj = Case.objects.get(pk=obj.pk)
                old_approved = old_obj.approved_amount or Decimal("0")

            delta = new_approved - old_approved
            if delta < 0:
                delta = Decimal("0")

            platform_total = (
                Donation.objects.filter(
                    paid=True,
                    donation_type="PLATFORM",
                    case__isnull=True,
                ).aggregate(total=Sum("amount"))["total"]
                or Decimal("0")
            )

            allocated_total = (
                Case.objects.exclude(pk=obj.pk)
                .filter(approved_amount__isnull=False)
                .aggregate(total=Sum("approved_amount"))["total"]
                or Decimal("0")
            )

            available_balance = platform_total - allocated_total

            if delta > available_balance:
                raise ValidationError(
                    f"Insufficient platform balance. Available: £{available_balance}. "
                    f"Requested approval increase: £{delta}."
                )

            # Record the admin who approved the case
            if obj.approved_amount and obj.approved_amount > 0 and obj.approved_by is None:
                obj.approved_by = request.user

        super().save_model(request, obj, form, change)