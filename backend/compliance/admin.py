
from django.contrib import admin

from .models import ComplianceResult


@admin.register(ComplianceResult)
class ComplianceResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "bid",
        "requirement",
        "status",
        "risk_level",
        "confidence_score",
        "reviewed_by",
        "created_at",
    )

    list_filter = (
        "status",
        "risk_level",
        "created_at",
    )

    search_fields = (
        "bid__tender__title",
        "bid__tender__reference_number",
        "bid__bidder__email",
        "requirement__title",
        "evidence_text",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
