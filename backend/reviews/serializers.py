
from rest_framework import serializers

from .models import ComplianceReview


class ComplianceReviewSerializer(serializers.ModelSerializer):

    compliance_status = serializers.CharField(
        source="compliance_result.status",
        read_only=True
    )

    requirement_title = serializers.CharField(
        source="compliance_result.requirement.title",
        read_only=True
    )

    bid_reference = serializers.CharField(
        source="compliance_result.bid.tender.reference_number",
        read_only=True
    )

    reviewer_email = serializers.EmailField(
        source="reviewer.email",
        read_only=True
    )

    class Meta:
        model = ComplianceReview

        fields = [
            "id",
            "compliance_result",
            "compliance_status",
            "requirement_title",
            "bid_reference",
            "reviewer",
            "reviewer_email",
            "decision",
            "comments",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "compliance_status",
            "requirement_title",
            "bid_reference",
            "reviewer",
            "reviewer_email",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]

    def validate_comments(self, value):
        return value.strip()
