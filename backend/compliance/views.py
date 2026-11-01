
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from bidders.models import Bid
from requirements_engine.models import TenderRequirement
from .models import ComplianceResult
from .serializers import ComplianceResultSerializer


def can_manage_compliance(user):
    return user.is_superuser or user.role in [
        "ADMIN",
        "TENDER_MANAGER",
        "REVIEWER",
    ]


def validate_bid_requirement(bid_id, requirement_id):
    bid = get_object_or_404(Bid, pk=bid_id)

    requirement = get_object_or_404(
        TenderRequirement,
        pk=requirement_id
    )

    if bid.tender_id != requirement.tender_id:
        return None, None

    return bid, requirement


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def compliance_list_create(request):

    if request.method == "GET":

        if not can_manage_compliance(request.user):
            results = ComplianceResult.objects.filter(
                bid__bidder=request.user
            )
        else:
            results = ComplianceResult.objects.all()

        results = results.select_related(
            "bid",
            "bid__tender",
            "requirement",
            "document",
            "reviewed_by",
        )

        bid_id = request.query_params.get("bid")

        if bid_id:
            results = results.filter(bid_id=bid_id)

        serializer = ComplianceResultSerializer(
            results,
            many=True
        )

        return Response(serializer.data)

    if not can_manage_compliance(request.user):
        return Response(
            {"message": "You do not have permission to create compliance results."},
            status=status.HTTP_403_FORBIDDEN
        )

    bid_id = request.data.get("bid")
    requirement_id = request.data.get("requirement")

    if not bid_id or not requirement_id:
        return Response(
            {
                "message": "Both bid and requirement are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    bid, requirement = validate_bid_requirement(
        bid_id,
        requirement_id
    )

    if bid is None:
        return Response(
            {
                "message": "The requirement does not belong to the bid's tender."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if ComplianceResult.objects.filter(
        bid=bid,
        requirement=requirement
    ).exists():
        return Response(
            {
                "message": "A compliance result already exists for this bid and requirement."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ComplianceResultSerializer(data=request.data)

    if serializer.is_valid():
        document_id = request.data.get("document")

        if document_id:
            from documents.models import BidDocument

            document = get_object_or_404(
                BidDocument,
                pk=document_id
            )

            if document.bid_id != bid.id:
                return Response(
                    {
                        "message": "The selected document does not belong to this bid."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        result = serializer.save(
            reviewed_by=request.user
        )

        return Response(
            ComplianceResultSerializer(result).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def compliance_detail(request, pk):

    result = get_object_or_404(
        ComplianceResult.objects.select_related(
            "bid",
            "bid__tender",
            "requirement",
            "document",
            "reviewed_by",
        ),
        pk=pk
    )

    if (
        result.bid.bidder_id != request.user.id
        and not can_manage_compliance(request.user)
    ):
        return Response(
            {"message": "You do not have permission to view this result."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":
        serializer = ComplianceResultSerializer(result)
        return Response(serializer.data)

    if not can_manage_compliance(request.user):
        return Response(
            {"message": "You do not have permission to modify compliance results."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "DELETE":
        result.delete()

        return Response(
            {"message": "Compliance result deleted successfully."},
            status=status.HTTP_200_OK
        )

    serializer = ComplianceResultSerializer(
        result,
        data=request.data,
        partial=(request.method == "PATCH")
    )

    if serializer.is_valid():

        bid_id = request.data.get("bid", result.bid_id)
        requirement_id = request.data.get(
            "requirement",
            result.requirement_id
        )

        bid, requirement = validate_bid_requirement(
            bid_id,
            requirement_id
        )

        if bid is None:
            return Response(
                {
                    "message": "The requirement does not belong to the bid's tender."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        document_id = request.data.get(
            "document",
            result.document_id
        )

        if document_id:
            from documents.models import BidDocument

            document = get_object_or_404(
                BidDocument,
                pk=document_id
            )

            if document.bid_id != bid.id:
                return Response(
                    {
                        "message": "The selected document does not belong to this bid."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        updated_result = serializer.save()

        return Response(
            ComplianceResultSerializer(updated_result).data
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
