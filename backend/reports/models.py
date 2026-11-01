
from django.conf import settings
from django.db import models


class ComplianceReport(models.Model):

    class ReportStatus(models.TextChoices):
        GENERATED = "GENERATED", "Generated"
        FAILED = "FAILED", "Failed"

    bid = models.ForeignKey(
        "bidders.Bid",
        on_delete=models.CASCADE,
        related_name="compliance_reports"
    )

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="generated_compliance_reports"
    )

    total_requirements = models.PositiveIntegerField(default=0)

    compliant_count = models.PositiveIntegerField(default=0)

    non_compliant_count = models.PositiveIntegerField(default=0)

    missing_count = models.PositiveIntegerField(default=0)

    needs_review_count = models.PositiveIntegerField(default=0)

    overall_risk_level = models.CharField(
        max_length=20,
        default="MEDIUM"
    )

    summary = models.TextField(blank=True)

    report_file = models.FileField(
        upload_to="compliance_reports/%Y/%m/",
        null=True,
        blank=True
    )

    report_status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.GENERATED
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return (
            f"Compliance Report #{self.id} - "
            f"Bid #{self.bid_id}"
        )
