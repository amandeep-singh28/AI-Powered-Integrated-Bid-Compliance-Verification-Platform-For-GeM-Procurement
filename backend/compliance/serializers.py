
from rest_framework import serializers

from .models import ComplianceResult


class ComplianceResultSerializer(serializers.ModelSerializer):

    bid_reference = serializers.CharField(
        source="bid.tender.reference_number",
        read_only=True
    )

    requirement_title = serializers.CharField(
        source="requirement.title",
        read_only=True
    )

    requirement_category = serializers.CharField(
        source="requirement.category",
        read_only=True
    )

    document_title = serializers.CharField(
        source="document.title",
        read_only=True,
        allow_null=True
    )

    reviewed_by_email = serializers.EmailField(
        source="reviewed_by.email",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = ComplianceResult

        fields = [
            "id",
            "bid",
            "bid_reference",
            "requirement",
            "requirement_title",
            "requirement_category",
            "document",
            "document_title",
            "evidence_text",
            "reference_page",
            "status",
            "risk_level",
            "confidence_score",
            "explanation",
            "recommendation",
            "reviewed_by",
            "reviewed_by_email",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "bid_reference",
            "requirement_title",
            "requirement_category",
            "document_title",
            "reviewed_by",
            "reviewed_by_email",
            "created_at",
            "updated_at",
        ]

    def validate_confidence_score(self, value):
        if value is not None and not 0 <= value <= 1:
            raise serializers.ValidationError(
                "Confidence score must be between 0 and 1."
            )
        return value

    def validate_reference_page(self, value):
        if value is not None and value < 1:
            raise serializers.ValidationError(
                "Reference page must be 1 or greater."
            )
        return value
