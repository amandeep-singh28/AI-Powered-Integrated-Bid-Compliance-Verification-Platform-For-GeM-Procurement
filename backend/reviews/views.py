
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from compliance.models import ComplianceResult
from .models import ComplianceReview
from .serializers import ComplianceReviewSerializer


def can_review(user):
    return user.is_superuser or user.role in [
        "ADMIN",
        "REVIEWER",
    ]


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def review_list_create(request):

    if not can_review(request.user):
        return Response(
            {"message": "Only administrators and reviewers can access this module."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":

        reviews = ComplianceReview.objects.select_related(
            "compliance_result",
            "compliance_result__bid",
            "compliance_result__bid__tender",
            "compliance_result__requirement",
            "reviewer",
        )

        decision = request.query_params.get("decision")

        if decision:
            reviews = reviews.filter(decision=decision)

        serializer = ComplianceReviewSerializer(
            reviews,
            many=True
        )

        return Response(serializer.data)

    compliance_result_id = request.data.get("compliance_result")

    if not compliance_result_id:
        return Response(
            {"compliance_result": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST
        )

    compliance_result = get_object_or_404(
        ComplianceResult,
        pk=compliance_result_id
    )

    if ComplianceReview.objects.filter(
        compliance_result=compliance_result,
        decision="PENDING"
    ).exists():
        return Response(
            {"message": "A pending review already exists for this result."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ComplianceReviewSerializer(data=request.data)

    if serializer.is_valid():

        decision = serializer.validated_data.get(
            "decision",
            ComplianceReview.Decision.PENDING
        )

        reviewed_at = (
            timezone.now()
            if decision in [
                ComplianceReview.Decision.APPROVED,
                ComplianceReview.Decision.REJECTED,
            ]
            else None
        )

        review = serializer.save(
            reviewer=request.user,
            reviewed_at=reviewed_at
        )

        return Response(
            ComplianceReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def review_detail(request, pk):

    if not can_review(request.user):
        return Response(
            {"message": "Only administrators and reviewers can access this module."},
            status=status.HTTP_403_FORBIDDEN
        )

    review = get_object_or_404(
        ComplianceReview.objects.select_related(
            "compliance_result",
            "compliance_result__bid",
            "compliance_result__bid__tender",
            "compliance_result__requirement",
            "reviewer",
        ),
        pk=pk
    )

    if request.method == "GET":
        serializer = ComplianceReviewSerializer(review)
        return Response(serializer.data)

    serializer = ComplianceReviewSerializer(
        review,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        decision = serializer.validated_data.get(
            "decision",
            review.decision
        )

        reviewed_at = review.reviewed_at

        if decision in [
            ComplianceReview.Decision.APPROVED,
            ComplianceReview.Decision.REJECTED,
        ]:
            reviewed_at = timezone.now()

        elif decision == ComplianceReview.Decision.PENDING:
            reviewed_at = None

        updated_review = serializer.save(
            reviewed_at=reviewed_at
        )

        return Response(
            ComplianceReviewSerializer(updated_review).data
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
