
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from bidders.models import Bid
from compliance.models import ComplianceResult
from .models import ComplianceReport
from .serializers import ComplianceReportSerializer


def can_generate_reports(user):
    return user.is_superuser or user.role in [
        "ADMIN",
        "TENDER_MANAGER",
        "REVIEWER",
    ]


def calculate_risk_level(results):
    if results.filter(
        risk_level="CRITICAL"
    ).exists():
        return "CRITICAL"

    if results.filter(
        risk_level="HIGH"
    ).exists():
        return "HIGH"

    if results.filter(
        risk_level="MEDIUM"
    ).exists():
        return "MEDIUM"

    return "LOW"


def generate_report_summary(
    total,
    compliant,
    non_compliant,
    missing,
    needs_review,
    risk_level
):
    return (
        f"Compliance assessment completed on "
        f"{timezone.now().strftime('%d-%m-%Y %H:%M')}. "
        f"Total evaluated requirements: {total}. "
        f"Compliant: {compliant}. "
        f"Non-compliant: {non_compliant}. "
        f"Missing: {missing}. "
        f"Needs review: {needs_review}. "
        f"Overall risk level: {risk_level}."
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def report_list_create(request):

    if request.method == "GET":

        if can_generate_reports(request.user):
            reports = ComplianceReport.objects.select_related(
                "bid",
                "bid__tender",
                "bid__bidder",
                "generated_by"
            ).all()
        else:
            reports = ComplianceReport.objects.filter(
                bid__bidder=request.user
            ).select_related(
                "bid",
                "bid__tender",
                "bid__bidder",
                "generated_by"
            )

        serializer = ComplianceReportSerializer(
            reports,
            many=True
        )

        return Response(serializer.data)

    if not can_generate_reports(request.user):
        return Response(
            {"message": "You do not have permission to generate reports."},
            status=status.HTTP_403_FORBIDDEN
        )

    bid_id = request.data.get("bid")

    if not bid_id:
        return Response(
            {"bid": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST
        )

    bid = get_object_or_404(Bid, pk=bid_id)

    results = ComplianceResult.objects.filter(
        bid=bid
    )

    counts = results.aggregate(
        total=Count("id"),
        compliant=Count(
            "id",
            filter=__import__(
                "django.db.models",
                fromlist=["Q"]
            ).Q(status="COMPLIANT")
        ),
        non_compliant=Count(
            "id",
            filter=__import__(
                "django.db.models",
                fromlist=["Q"]
            ).Q(status="NON_COMPLIANT")
        ),
        missing=Count(
            "id",
            filter=__import__(
                "django.db.models",
                fromlist=["Q"]
            ).Q(status="MISSING")
        ),
        needs_review=Count(
            "id",
            filter=__import__(
                "django.db.models",
                fromlist=["Q"]
            ).Q(status="NEEDS_REVIEW")
        )
    )

    risk_level = calculate_risk_level(results)

    summary = generate_report_summary(
        counts["total"],
        counts["compliant"],
        counts["non_compliant"],
        counts["missing"],
        counts["needs_review"],
        risk_level
    )

    report = ComplianceReport.objects.create(
        bid=bid,
        generated_by=request.user,
        total_requirements=counts["total"],
        compliant_count=counts["compliant"],
        non_compliant_count=counts["non_compliant"],
        missing_count=counts["missing"],
        needs_review_count=counts["needs_review"],
        overall_risk_level=risk_level,
        summary=summary
    )

    return Response(
        ComplianceReportSerializer(report).data,
        status=status.HTTP_201_CREATED
    )


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def report_detail(request, pk):

    report = get_object_or_404(
        ComplianceReport.objects.select_related(
            "bid",
            "bid__tender",
            "bid__bidder",
            "generated_by"
        ),
        pk=pk
    )

    if (
        report.bid.bidder_id != request.user.id
        and not can_generate_reports(request.user)
    ):
        return Response(
            {"message": "You do not have permission to access this report."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":
        serializer = ComplianceReportSerializer(report)
        return Response(serializer.data)

    if not can_generate_reports(request.user):
        return Response(
            {"message": "You do not have permission to delete reports."},
            status=status.HTTP_403_FORBIDDEN
        )

    report.delete()

    return Response(
        {"message": "Report deleted successfully."},
        status=status.HTTP_200_OK
    )
