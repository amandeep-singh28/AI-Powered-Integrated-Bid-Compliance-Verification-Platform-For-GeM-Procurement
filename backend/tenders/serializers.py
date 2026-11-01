
from rest_framework import serializers
from .models import Tender


class TenderSerializer(serializers.ModelSerializer):

    created_by_email = serializers.EmailField(
        source="created_by.email",
        read_only=True,
    )

    class Meta:
        model = Tender
        fields = [
            "id",
            "title",
            "reference_number",
            "description",
            "department",
            "category",
            "estimated_value",
            "published_at",
            "submission_deadline",
            "status",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",
        ]

    def validate_reference_number(self, value):
        return value.strip().upper()

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Tender title cannot be empty."
            )

        return value

    def validate(self, data):
        published_at = data.get("published_at")
        deadline = data.get("submission_deadline")

        if published_at and deadline and deadline <= published_at:
            raise serializers.ValidationError({
                "submission_deadline":
                    "The submission deadline must be after the publication date."
            })

        return data
