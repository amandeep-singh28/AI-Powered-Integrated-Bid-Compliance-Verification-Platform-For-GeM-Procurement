
from pathlib import Path

from rest_framework import serializers

from .models import BidDocument, TenderDocument


class BidDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(
        source="uploaded_by.email",
        read_only=True,
    )

    bid_reference = serializers.CharField(
        source="bid.tender.reference_number",
        read_only=True,
    )

    class Meta:
        model = BidDocument
        fields = [
            "id",
            "bid",
            "bid_reference",
            "uploaded_by",
            "uploaded_by_email",
            "document_type",
            "title",
            "file",
            "original_filename",
            "processing_status",
            "extracted_text",
            "uploaded_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_by_email",
            "bid_reference",
            "original_filename",
            "processing_status",
            "extracted_text",
            "uploaded_at",
            "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Document title cannot be empty."
            )

        return value

    def validate_file(self, value):
        allowed_extensions = [".pdf", ".doc", ".docx", ".txt"]
        extension = Path(value.name).suffix.lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOC, DOCX, and TXT files are allowed."
            )

        max_size = 10 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                "File size cannot exceed 10 MB."
            )

        return value







class TenderDocumentSerializer(serializers.ModelSerializer):

    tender_reference = serializers.CharField(
        source="tender.reference_number",
        read_only=True
    )

    uploaded_by_email = serializers.EmailField(
        source="uploaded_by.email",
        read_only=True
    )

    class Meta:
        model = TenderDocument

        fields = [
            "id",
            "tender",
            "tender_reference",
            "uploaded_by",
            "uploaded_by_email",
            "title",
            "file",
            "original_filename",
            "extracted_text",
            "processing_status",
            "uploaded_at",
            "updated_at"
        ]

        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_by_email",
            "tender_reference",
            "original_filename",
            "extracted_text",
            "processing_status",
            "uploaded_at",
            "updated_at"
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Document title cannot be empty."
            )

        return value

    def validate_file(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF files are allowed for tender documents."
            )

        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size cannot exceed 10 MB."
            )

        return value
