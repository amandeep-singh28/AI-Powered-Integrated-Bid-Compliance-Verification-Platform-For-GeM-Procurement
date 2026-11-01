
from django.conf import settings
from django.db import models


class BidDocument(models.Model):
    class DocumentType(models.TextChoices):
        TECHNICAL = "TECHNICAL", "Technical Document"
        FINANCIAL = "FINANCIAL", "Financial Document"
        ELIGIBILITY = "ELIGIBILITY", "Eligibility Document"
        EXPERIENCE = "EXPERIENCE", "Experience Certificate"
        CERTIFICATION = "CERTIFICATION", "Certification"
        OTHER = "OTHER", "Other"

    class ProcessingStatus(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        PROCESSED = "PROCESSED", "Processed"
        FAILED = "FAILED", "Processing Failed"

    bid = models.ForeignKey(
        "bidders.Bid",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_bid_documents",
    )

    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )

    title = models.CharField(max_length=255)

    file = models.FileField(upload_to="bid_documents/%Y/%m/")

    original_filename = models.CharField(max_length=255, blank=True)

    processing_status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.UPLOADED,
    )

    extracted_text = models.TextField(blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            self.original_filename = self.file.name.split("/")[-1].split("\\")[-1]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - Bid #{self.bid_id}"







class TenderDocument(models.Model):

    class ProcessingStatus(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        PROCESSED = "PROCESSED", "Processed"
        FAILED = "FAILED", "Processing Failed"

    tender = models.ForeignKey(
        "tenders.Tender",
        on_delete=models.CASCADE,
        related_name="tender_documents"
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_tender_documents"
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to="tender_documents/%Y/%m/"
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True
    )

    extracted_text = models.TextField(blank=True)

    processing_status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.UPLOADED
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            self.original_filename = (
                self.file.name.split("/")[-1].split("\\")[-1]
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.tender.reference_number}"
