from cloudinary.models import CloudinaryField
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
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

    ANIMAL_CHOICES = [
        ("CAT", "Cat"),
        ("DOG", "Dog"),
    ]

    ANIMALS_COUNT_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
        (11, "Other (please specify in description)"),
    ]

    TITLE_CHOICES = [
        ("FOOD", "Food"),
        ("NEUTERING", "Neutering"),
        ("SURGERY", "Surgery"),
        ("URGENT SURGERY", "Urgent surgery"),
        ("PRESCRIPTION_FOOD", "Vet prescription food"),
        ("OTHER_VET_SERVICE", "Other vet service"),
        ("FLEA_TREATMENT", "Flea treatment"),
        ("TRANSPORT", "Transport expenses"),
        ("OTHER", "Other"),
    ]

    PAYOUT_METHOD_CHOICES = [
        ("BANK", "Bank transfer"),
        ("PAYPAL", "PayPal"),
    ]

    shelter = models.ForeignKey(
        "shelters.Shelter",
        on_delete=models.CASCADE,
        related_name="cases",
    )

    title = models.CharField(
        max_length=30,
        choices=TITLE_CHOICES,
        default="FOOD",
    )

    animal = models.CharField(
        max_length=10,
        choices=ANIMAL_CHOICES,
        default="CAT",
    )

    animal_names = models.CharField(
        max_length=255,
        blank=True,
        help_text="Write all animal names you know, or give temporary names if needed.",
    )

    animals_count = models.PositiveSmallIntegerField(
        choices=ANIMALS_COUNT_CHOICES,
        default=1,
    )

    description = models.TextField(
        help_text="Please provide as many details as possible about the animals, their condition, and how the requested funds will be used.",
        validators=[
            MinLengthValidator(120, message="Please provide a detailed description.")
        ],
    )

    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)

    amount_funded = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    approved_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="When admin approves an amount greater than 0, the case will move from OPEN to PROCESSING.",
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    approved_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_cases",
    )

    payout_method = models.CharField(
        max_length=20,
        choices=PAYOUT_METHOD_CHOICES,
        blank=True,
        default="",
        help_text="Select how funds will be sent (Bank transfer or PayPal).",
    )

    payout_reference = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Provide bank details or PayPal email.",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    proof_link = models.URLField(blank=True)

    processing_started_at = models.DateTimeField(null=True, blank=True)
    proof_due_at = models.DateTimeField(null=True, blank=True)
    proof_submitted_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_title_display()

    @property
    def is_overdue(self):
        return bool(
            self.proof_due_at
            and timezone.now() > self.proof_due_at
            and self.status == "PROCESSING"
        )

    @property
    def funding_progress(self):
        if self.amount_requested == 0:
            return 0
        return int((self.amount_funded / self.amount_requested) * 100)

    def clean(self):
        if self.status == "PROCESSING":
            if not self.approved_amount or self.approved_amount <= 0:
                raise ValidationError("Approved amount is required for processing.")

            if not self.payout_method:
                raise ValidationError("Please select payout method.")

            if not self.payout_reference:
                raise ValidationError("Please provide payout reference.")

            if not self.approved_by:
                raise ValidationError("Approved by is required when approving the case.")

        if self.status == "AWAITING_REVIEW" and not self.proof_link:
            raise ValidationError("Proof link is required for review.")

        if self.status == "CLOSED" and not self.proof_link:
            raise ValidationError("Cannot close without proof.")

        super().clean()

    def save(self, *args, **kwargs):
        previous = None
        if self.pk:
            previous = Case.objects.filter(pk=self.pk).only(
                "status",
                "approved_amount",
                "proof_link",
                "processing_started_at",
                "proof_due_at",
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
            if entering_processing:
                if self.processing_started_at is None:
                    self.processing_started_at = now
                if self.proof_due_at is None:
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
            shelter.trust_points = (shelter.trust_points or 0) + 1
            shelter.save(update_fields=["trust_points"])
            shelter.update_verification()


class CaseImage(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = CloudinaryField("image", folder="openpaws/case_images")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.case.get_title_display()}"

    def clean(self):
        if self.case_id:
            existing_count = self.case.images.exclude(pk=self.pk).count()
            if existing_count >= 3:
                raise ValidationError("Maximum 3 images allowed.")