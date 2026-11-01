
from django.contrib import admin
from .models import TenderRequirement


@admin.register(TenderRequirement)
class TenderRequirementAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "tender",
        "category",
        "priority",
        "reference_page",
        "created_at",
    )

    list_filter = (
        "category",
        "priority",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "tender__title",
        "tender__reference_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("category", "id")
