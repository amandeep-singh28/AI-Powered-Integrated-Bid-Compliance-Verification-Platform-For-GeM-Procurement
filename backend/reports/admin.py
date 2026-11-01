
from django.contrib import admin

from .models import ComplianceReport


@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "bid",
        "generated_by",
        "total_requirements",
        "compliant_count",
        "non_compliant_count",
        "missing_count",
        "needs_review_count",
        "overall_risk_level",
        "report_status",
        "generated_at",
    )

    list_filter = (
        "overall_risk_level",
        "report_status",
        "generated_at",
    )

    search_fields = (
        "bid__tender__title",
        "bid__tender__reference_number",
        "bid__bidder__email",
        "generated_by__email",
    )

    readonly_fields = (
        "total_requirements",
        "compliant_count",
        "non_compliant_count",
        "missing_count",
        "needs_review_count",
        "overall_risk_level",
        "report_file",
        "report_status",
        "generated_at",
        "updated_at",
    )

    ordering = ("-generated_at",)
