from django.db import models
from django.contrib.auth.models import User


class Donation(models.Model):
    DONATION_TYPES = [
        ("PLATFORM", "Platform"),
        ("CASE", "Case"),
        ("THANK_YOU", "Thank You"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    case = models.ForeignKey(
        "cases.Case",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )

    shelter = models.ForeignKey(
        "shelters.Shelter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thank_you_donations",
    )

    donation_type = models.CharField(
        max_length=20,
        choices=DONATION_TYPES,
        default="PLATFORM",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"£{self.amount} donation ({self.donation_type})"