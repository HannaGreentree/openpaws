from django.contrib import admin
from .models import Shelter


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "trust_points", "is_verified")
    list_filter = ("country", "is_verified")
    search_fields = ("name", "city", "country", "email")
    readonly_fields = ("trust_points",)  # IMPORTANT: stops manual editing
