from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Case(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("PROCESSING", "Processing"),
        ("AWAITING_REVIEW", "Awaiting Review"),
        ("CLOSED", "Closed"),
        ("REJECTED", "Rejected"),
    ]

    shelter = models.ForeignKey("shelters.Shelter", on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_funded = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_cases",
    )

    payout_method = models.CharField(max_length=50, blank=True)
    payout_reference = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    proof_link = models.URLField(blank=True)

    processing_started_at = models.DateTimeField(null=True, blank=True)
    proof_due_at = models.DateTimeField(null=True, blank=True)
    proof_submitted_at = models.DateTimeField(null=True, blank=True)

    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self) -> bool:
        return bool(
            self.proof_due_at
            and timezone.now() > self.proof_due_at
            and self.status == "PROCESSING"
        )

    def clean(self):
        if self.status == "PROCESSING":
            if self.approved_amount is None or self.approved_amount <= 0:
                raise ValidationError(
                    "Cannot set status to PROCESSING without an approved amount greater than 0."
                )

        if self.status == "AWAITING_REVIEW" and not self.proof_link:
            raise ValidationError("Cannot set status to AWAITING_REVIEW without a proof link.")

        if self.status == "CLOSED" and not self.proof_link:
            raise ValidationError("Cannot close a case without a proof link.")

        return super().clean()

    def save(self, *args, **kwargs):
        previous = None
        if self.pk:
            previous = Case.objects.filter(pk=self.pk).only(
                "status",
                "approved_amount",
                "proof_link",
                "processing_started_at",
                "proof_submitted_at",
                "closed_at",
                "approved_at",
            ).first()

        now = timezone.now()

        if self.approved_amount and self.approved_amount > 0 and self.status == "OPEN":
            self.status = "PROCESSING"
            if self.approved_at is None:
                self.approved_at = now

        if self.status == "PROCESSING":
            entering_processing = previous is None or previous.status != "PROCESSING"
            if entering_processing and self.processing_started_at is None:
                self.processing_started_at = now
                self.proof_due_at = now + timedelta(days=14)

        if self.proof_link and self.status == "PROCESSING":
            self.status = "AWAITING_REVIEW"
            if self.proof_submitted_at is None:
                self.proof_submitted_at = now

        entering_closed = self.status == "CLOSED" and (
            previous is None or previous.status != "CLOSED"
        )

        if entering_closed and self.closed_at is None:
            self.closed_at = now

        super().save(*args, **kwargs)

        if entering_closed:
            shelter = self.shelter
            shelter.trust_points += 1
            shelter.save(update_fields=["trust_points"])