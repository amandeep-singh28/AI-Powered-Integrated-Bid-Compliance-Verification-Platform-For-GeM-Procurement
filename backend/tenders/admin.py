
from django.contrib import admin
from .models import Tender


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reference_number",
        "title",
        "department",
        "status",
        "submission_deadline",
        "created_by",
        "created_at",
    )

    list_filter = (
        "status",
        "department",
        "category",
        "created_at",
    )

    search_fields = (
        "reference_number",
        "title",
        "department",
        "description",
        "created_by__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
