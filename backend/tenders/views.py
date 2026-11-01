
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Tender
from .serializers import TenderSerializer


def is_tender_authority(user):
    return user.is_authenticated and (
        user.is_superuser or user.role in ["ADMIN", "TENDER_MANAGER"]
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def tender_list_create(request):
    if request.method == "GET":
        if is_tender_authority(request.user):
            tenders = Tender.objects.all()
        else:
            tenders = Tender.objects.exclude(status=Tender.Status.DRAFT)

        serializer = TenderSerializer(tenders, many=True)
        return Response(serializer.data)

    if not is_tender_authority(request.user):
        return Response(
            {"message": "Only Admin and Tender Manager can create tenders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = TenderSerializer(data=request.data)

    if serializer.is_valid():
        tender_status = serializer.validated_data.get(
            "status", Tender.Status.DRAFT
        )
        extra_fields = {"created_by": request.user}

        if tender_status == Tender.Status.PUBLISHED:
            extra_fields["published_at"] = timezone.now()

        tender = serializer.save(**extra_fields)
        return Response(
            TenderSerializer(tender).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def tender_detail(request, pk):
    tender = get_object_or_404(Tender, pk=pk)

    if request.method == "GET":
        if (
            tender.status == Tender.Status.DRAFT
            and not is_tender_authority(request.user)
        ):
            return Response(
                {"message": "This tender is not available."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(TenderSerializer(tender).data)

    if not is_tender_authority(request.user):
        return Response(
            {"message": "Only Admin and Tender Manager can update tenders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = TenderSerializer(
        tender,
        data=request.data,
        partial=(request.method == "PATCH"),
    )

    if serializer.is_valid():
        updated_tender = serializer.save()

        if (
            updated_tender.status == Tender.Status.PUBLISHED
            and not updated_tender.published_at
        ):
            updated_tender.published_at = timezone.now()
            updated_tender.save(update_fields=["published_at"])

        return Response(TenderSerializer(updated_tender).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
