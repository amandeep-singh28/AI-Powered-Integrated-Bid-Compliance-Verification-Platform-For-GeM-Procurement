
from django.urls import path

from .views import (
    document_list_create,
    document_detail,
    tender_document_list_create,
    tender_document_detail,
)

urlpatterns = [
    # Bidder Documents
    path("", document_list_create, name="document-list-create"),
    path("<int:pk>/", document_detail, name="document-detail"),

    # Original Tender Documents
    path(
        "tenders/",
        tender_document_list_create,
        name="tender-document-list-create"
    ),
    path(
        "tenders/<int:pk>/",
        tender_document_detail,
        name="tender-document-detail"
    ),
]
