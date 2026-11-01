
from rest_framework import serializers

from .models import ComplianceReport


class ComplianceReportSerializer(serializers.ModelSerializer):

    bid_reference = serializers.CharField(
        source="bid.tender.reference_number",
        read_only=True
    )

    tender_title = serializers.CharField(
        source="bid.tender.title",
        read_only=True
    )

    bidder_email = serializers.EmailField(
        source="bid.bidder.email",
        read_only=True
    )

    generated_by_email = serializers.EmailField(
        source="generated_by.email",
        read_only=True
    )

    class Meta:
        model = ComplianceReport

        fields = [
            "id",
            "bid",
            "bid_reference",
            "tender_title",
            "bidder_email",
            "generated_by",
            "generated_by_email",
            "total_requirements",
            "compliant_count",
            "non_compliant_count",
            "missing_count",
            "needs_review_count",
            "overall_risk_level",
            "summary",
            "report_file",
            "report_status",
            "generated_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "bid_reference",
            "tender_title",
            "bidder_email",
            "generated_by",
            "generated_by_email",
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
        ]
