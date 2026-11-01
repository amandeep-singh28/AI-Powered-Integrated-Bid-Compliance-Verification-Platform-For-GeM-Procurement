
from django.contrib import admin

from .models import ComplianceReview


@admin.register(ComplianceReview)
class ComplianceReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "compliance_result",
        "reviewer",
        "decision",
        "reviewed_at",
        "created_at",
    )

    list_filter = (
        "decision",
        "reviewed_at",
        "created_at",
    )

    search_fields = (
        "reviewer__email",
        "compliance_result__requirement__title",
        "compliance_result__bid__tender__reference_number",
        "comments",
    )

    readonly_fields = (
        "reviewed_at",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
