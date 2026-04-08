from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import Case, CaseImage


class CaseImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        total_images = 0

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            if form.cleaned_data.get("image"):
                total_images += 1
            elif form.instance and form.instance.pk:
                total_images += 1

        if total_images > 3:
            raise ValidationError("Maximum 3 images are allowed per case.")


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    formset = CaseImageInlineFormSet
    extra = 0
    max_num = 3
    verbose_name = "Image"
    verbose_name_plural = "Images"


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        "display_title",
        "animal",
        "animals_count",
        "shelter",
        "status",
        "amount_requested",
        "amount_funded",
        "approved_amount",
        "proof_received",
        "is_overdue_display",
        "approved_by",
        "approved_at",
        "created_at",
    )

    list_display_links = ("display_title",)

    list_filter = (
        "status",
        "animal",
        "shelter",
        "approved_at",
        "created_at",
        "closed_at",
    )

    search_fields = (
        "animal_names",
        "description",
        "shelter__name",
        "payout_reference",
    )

    readonly_fields = (
        "approved_by",
        "created_at",
        "approved_at",
        "processing_started_at",
        "proof_due_at",
        "proof_submitted_at",
        "closed_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Case Information", {
            "fields": (
                "shelter",
                "title",
                "animal",
                "animal_names",
                "animals_count",
                "description",
                "status",
            )
        }),
        ("Funding", {
            "fields": (
                "amount_requested",
                "amount_funded",
                "approved_amount",
            )
        }),
        ("Approval", {
            "fields": (
                "approved_by",
                "approved_at",
            )
        }),
        ("Payout", {
            "fields": (
                "payout_method",
                "payout_reference",
            )
        }),
        ("Proof", {
            "fields": (
                "proof_link",
                "processing_started_at",
                "proof_due_at",
                "proof_submitted_at",
            )
        }),
        ("Closure", {
            "fields": (
                "closed_at",
                "created_at",
            )
        }),
    )

    inlines = [CaseImageInline]

    actions = ["mark_as_rejected", "mark_as_closed"]

    def save_model(self, request, obj, form, change):
        old_status = None
        if obj.pk:
            old_case = Case.objects.filter(pk=obj.pk).first()
            if old_case:
                old_status = old_case.status

        if obj.approved_amount and obj.approved_amount > 0:
            if not obj.approved_by:
                obj.approved_by = request.user

        super().save_model(request, obj, form, change)

        if obj.status == "CLOSED" and old_status != "CLOSED":
            obj.shelter.update_verification()

    @admin.display(description="Title")
    def display_title(self, obj):
        return obj.get_title_display() or obj.title

    @admin.display(boolean=True, description="Proof received")
    def proof_received(self, obj):
        return bool(obj.proof_link)

    @admin.display(boolean=True, description="Overdue")
    def is_overdue_display(self, obj):
        return obj.is_overdue

    @admin.action(description="Mark selected cases as Rejected")
    def mark_as_rejected(self, request, queryset):
        for case in queryset:
            case.status = "REJECTED"
            case.save()

    @admin.action(description="Mark selected cases as Closed")
    def mark_as_closed(self, request, queryset):
        for case in queryset:
            if case.proof_link:
                case.status = "CLOSED"
                case.save()


@admin.register(CaseImage)
class CaseImageAdmin(admin.ModelAdmin):
    list_display = ("case", "uploaded_at")
    search_fields = ("case__title",)
    ordering = ("-uploaded_at",)