
from django.contrib import admin

from .models import BidDocument, TenderDocument


@admin.register(BidDocument)
class BidDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "bid",
        "uploaded_by",
        "document_type",
        "processing_status",
        "uploaded_at",
    )

    list_filter = (
        "document_type",
        "processing_status",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "original_filename",
        "uploaded_by__email",
    )

    readonly_fields = (
        "original_filename",
        "extracted_text",
        "processing_status",
        "uploaded_at",
        "updated_at",
    )


@admin.register(TenderDocument)
class TenderDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "tender",
        "uploaded_by",
        "processing_status",
        "uploaded_at",
    )

    list_filter = (
        "processing_status",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "original_filename",
        "tender__reference_number",
        "uploaded_by__email",
    )

    readonly_fields = (
        "original_filename",
        "extracted_text",
        "processing_status",
        "uploaded_at",
        "updated_at",
    )
