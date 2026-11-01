
from django.contrib import admin
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tender",
        "bidder",
        "bid_amount",
        "status",
        "submitted_at",
    )

    list_filter = (
        "status",
        "submitted_at",
    )

    search_fields = (
        "tender__title",
        "tender__reference_number",
        "bidder__email",
    )

    readonly_fields = (
        "submitted_at",
        "updated_at",
    )

    ordering = ("-submitted_at",)
