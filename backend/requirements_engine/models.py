
from django.db import models


class TenderRequirement(models.Model):

    class Category(models.TextChoices):
        ELIGIBILITY = "ELIGIBILITY", "Eligibility"
        TECHNICAL = "TECHNICAL", "Technical"
        FINANCIAL = "FINANCIAL", "Financial"
        EXPERIENCE = "EXPERIENCE", "Experience"
        CERTIFICATION = "CERTIFICATION", "Certification"
        DOCUMENTATION = "DOCUMENTATION", "Documentation"

    class Priority(models.TextChoices):
        MANDATORY = "MANDATORY", "Mandatory"
        OPTIONAL = "OPTIONAL", "Optional"

    tender = models.ForeignKey(
        "tenders.Tender",
        on_delete=models.CASCADE,
        related_name="requirements",
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MANDATORY,
    )

    condition = models.TextField(blank=True)

    reference_page = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "id"]

    def __str__(self):
        return f"{self.title} - {self.tender.reference_number}"
