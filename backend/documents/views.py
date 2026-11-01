
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from bidders.models import Bid
from .models import BidDocument,TenderDocument
from .serializers import BidDocumentSerializer,TenderDocumentSerializer
from .utils import extract_text_from_pdf


def is_staff_role(user):
    return user.is_superuser or user.role in [
        "ADMIN",
        "TENDER_MANAGER",
        "REVIEWER",
    ]


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def document_list_create(request):
    if request.method == "GET":
        if is_staff_role(request.user):
            documents = BidDocument.objects.select_related(
                "bid", "bid__tender", "uploaded_by"
            ).all()
        else:
            documents = BidDocument.objects.filter(
                bid__bidder=request.user
            ).select_related("bid", "bid__tender", "uploaded_by")

        serializer = BidDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    if request.user.role != "BIDDER":
        return Response(
            {"message": "Only bidders can upload bid documents."},
            status=status.HTTP_403_FORBIDDEN,
        )

    bid_id = request.data.get("bid")

    if not bid_id:
        return Response(
            {"bid": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    bid = get_object_or_404(Bid, pk=bid_id)

    if bid.bidder_id != request.user.id:
        return Response(
            {"message": "You can upload documents only to your own bid."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = BidDocumentSerializer(data=request.data)

    if serializer.is_valid():
        document = serializer.save(
            bid=bid,
            uploaded_by=request.user,
        )

        if document.file.name.lower().endswith(".pdf"):
            try:
                extracted_text = extract_text_from_pdf(
                    document.file.path
                )

                document.extracted_text = extracted_text
                document.processing_status = (
                    BidDocument.ProcessingStatus.PROCESSED
                    if extracted_text.strip()
                    else BidDocument.ProcessingStatus.FAILED
                )

            except Exception:
                document.processing_status = (
                    BidDocument.ProcessingStatus.FAILED
                )

            document.save(
                update_fields=[
                    "extracted_text",
                    "processing_status",
                    "updated_at",
                ]
            )

        return Response(
            BidDocumentSerializer(document).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def document_detail(request, pk):
    document = get_object_or_404(
        BidDocument.objects.select_related(
            "bid", "bid__tender", "uploaded_by"
        ),
        pk=pk,
    )

    if (
        document.bid.bidder_id != request.user.id
        and not is_staff_role(request.user)
    ):
        return Response(
            {"message": "You do not have permission to view this document."},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response(BidDocumentSerializer(document).data)








def can_manage_tender_documents(user):
    return (
        user.is_superuser
        or user.role in ["ADMIN", "TENDER_MANAGER"]
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def tender_document_list_create(request):

    if request.method == "GET":

        if can_manage_tender_documents(request.user):
            documents = TenderDocument.objects.all()
        else:
            documents = TenderDocument.objects.filter(
                tender__status="PUBLISHED"
            )

        tender_id = request.query_params.get("tender")

        if tender_id:
            documents = documents.filter(tender_id=tender_id)

        serializer = TenderDocumentSerializer(
            documents,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    if not can_manage_tender_documents(request.user):
        return Response(
            {"error": "Only Admin and Tender Manager can upload tender documents."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = TenderDocumentSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():

        document = serializer.save(
            uploaded_by=request.user
        )

        try:
            extracted_text = extract_text_from_pdf(
                document.file.path
            )

            document.extracted_text = extracted_text

            if extracted_text.strip():
                document.processing_status = "PROCESSED"
            else:
                document.processing_status = "FAILED"

        except Exception:
            document.processing_status = "FAILED"

        document.save()

        response_serializer = TenderDocumentSerializer(
            document,
            context={"request": request}
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tender_document_detail(request, pk):

    document = get_object_or_404(
        TenderDocument,
        pk=pk
    )

    if (
        not can_manage_tender_documents(request.user)
        and document.tender.status != "PUBLISHED"
    ):
        return Response(
            {"error": "You do not have permission to view this document."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = TenderDocumentSerializer(
        document,
        context={"request": request}
    )

    return Response(serializer.data)
