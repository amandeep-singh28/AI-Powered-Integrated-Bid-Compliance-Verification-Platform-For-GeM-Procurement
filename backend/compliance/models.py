
from django.db import models


class ComplianceResult(models.Model):

    class Status(models.TextChoices):
        COMPLIANT = "COMPLIANT", "Compliant"
        NON_COMPLIANT = "NON_COMPLIANT", "Non-Compliant"
        MISSING = "MISSING", "Missing"
        NEEDS_REVIEW = "NEEDS_REVIEW", "Needs Review"

    class RiskLevel(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    bid = models.ForeignKey(
        "bidders.Bid",
        on_delete=models.CASCADE,
        related_name="compliance_results"
    )

    requirement = models.ForeignKey(
        "requirements_engine.TenderRequirement",
        on_delete=models.CASCADE,
        related_name="compliance_results"
    )

    document = models.ForeignKey(
        "documents.BidDocument",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="compliance_results"
    )

    evidence_text = models.TextField(blank=True)

    reference_page = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEEDS_REVIEW
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RiskLevel.choices,
        default=RiskLevel.MEDIUM
    )

    confidence_score = models.FloatField(
        null=True,
        blank=True
    )

    explanation = models.TextField(blank=True)

    recommendation = models.TextField(blank=True)

    reviewed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_compliance_results"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["bid", "requirement"],
                name="unique_compliance_per_bid_requirement"
            )
        ]

    def __str__(self):
        return (
            f"Bid #{self.bid_id} - "
            f"{self.requirement.title} - "
            f"{self.status}"
        )
