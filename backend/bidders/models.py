
from django.conf import settings
from django.db import models


class Bid(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    tender = models.ForeignKey(
        "tenders.Tender",
        on_delete=models.PROTECT,
        related_name="bids",
    )

    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="submitted_bids",
    )

    bid_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    proposal = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["tender", "bidder"],
                name="unique_bid_per_tender_bidder",
            )
        ]

    def __str__(self):
        return f"Bid #{self.id} - {self.tender.reference_number}"
