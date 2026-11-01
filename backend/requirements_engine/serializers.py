
from rest_framework import serializers
from .models import TenderRequirement


class TenderRequirementSerializer(serializers.ModelSerializer):

    tender_reference = serializers.CharField(
        source="tender.reference_number",
        read_only=True
    )

    class Meta:
        model = TenderRequirement

        fields = [
            "id",
            "tender",
            "tender_reference",
            "title",
            "description",
            "category",
            "priority",
            "condition",
            "reference_page",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "tender_reference",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Requirement title cannot be empty."
            )
        return value.strip()

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Requirement description cannot be empty."
            )
        return value.strip()

    def validate_reference_page(self, value):
        if value is not None and value < 1:
            raise serializers.ValidationError(
                "Reference page must be 1 or greater."
            )
        return value
