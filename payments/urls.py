from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("balance/", views.balance, name="balance"),

    # Platform donate
    path("donate/", views.donate_platform, name="donate_platform"),
    path("donate/checkout/", views.donate_platform_checkout, name="donate_platform_checkout"),

    # Thank you to shelter
    path("thank-you/<int:shelter_id>/", views.thank_you, name="thank_you"),
    path("thank-you/<int:shelter_id>/checkout/", views.thank_you_checkout, name="thank_you_checkout"),

    path("success/", views.payment_success, name="success"),
    path("cancel/", views.payment_cancel, name="cancel"),

    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]