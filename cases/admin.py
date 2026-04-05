from django.contrib import admin

from .models import Case, CaseImage


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 3


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
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
        if obj.approved_amount and obj.approved_amount > 0 and not obj.approved_by:
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(boolean=True, description="Proof received")
    def proof_received(self, obj):
        return bool(obj.proof_link)

    @admin.display(boolean=True, description="Overdue")
    def is_overdue_display(self, obj):
        return obj.is_overdue

    @admin.action(description="Mark selected cases as Rejected")
    def mark_as_rejected(self, request, queryset):
        queryset.update(status="REJECTED")

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