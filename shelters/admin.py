from django.contrib import admin
from .models import Shelter


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "trust_points", "is_verified")
    list_filter = ("country", "is_verified")
    search_fields = ("name", "city", "country", "email")
    readonly_fields = ("trust_points",)

    fields = (
        "owner",
        "name",
        "country",
        "city",
        "address",
        "email",
        "phone",
        "animals_count",
        "social_link_1",
        "social_link_2",
        "image",
        "trust_points",
        "is_verified",
    )