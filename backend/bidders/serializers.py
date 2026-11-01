
from rest_framework import serializers
from django.utils import timezone
from .models import Bid
from tenders.models import Tender


class BidSerializer(serializers.ModelSerializer):
    bidder_email = serializers.EmailField(
        source="bidder.email",
        read_only=True,
    )

    tender_reference = serializers.CharField(
        source="tender.reference_number",
        read_only=True,
    )

    class Meta:
        model = Bid
        fields = [
            "id",
            "tender",
            "tender_reference",
            "bidder",
            "bidder_email",
            "bid_amount",
            "proposal",
            "status",
            "submitted_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "bidder",
            "bidder_email",
            "tender_reference",
            "status",
            "submitted_at",
            "updated_at",
        ]

    def validate_bid_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Bid amount must be greater than zero."
            )
        return value

    def validate_proposal(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Bid proposal cannot be empty."
            )

        return value

    def validate_tender(self, tender):
        if tender.status != Tender.Status.PUBLISHED:
            raise serializers.ValidationError(
                "You can submit a bid only for a published tender."
            )

        if tender.submission_deadline <= timezone.now():
            raise serializers.ValidationError(
                "The submission deadline for this tender has passed."
            )

        return tender
