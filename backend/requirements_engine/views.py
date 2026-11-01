
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import TenderRequirement
from .serializers import TenderRequirementSerializer


def can_manage_requirements(user):
    return user.is_superuser or user.role in [
        "ADMIN",
        "TENDER_MANAGER",
    ]


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def requirement_list_create(request):

    if request.method == "GET":
        tender_id = request.query_params.get("tender")

        requirements = TenderRequirement.objects.select_related(
            "tender"
        ).all()

        if tender_id:
            requirements = requirements.filter(tender_id=tender_id)

        serializer = TenderRequirementSerializer(
            requirements,
            many=True
        )

        return Response(serializer.data)

    if not can_manage_requirements(request.user):
        return Response(
            {"message": "You do not have permission to create requirements."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = TenderRequirementSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def requirement_detail(request, pk):

    requirement = get_object_or_404(
        TenderRequirement.objects.select_related("tender"),
        pk=pk
    )

    if request.method == "GET":
        serializer = TenderRequirementSerializer(requirement)
        return Response(serializer.data)

    if not can_manage_requirements(request.user):
        return Response(
            {"message": "You do not have permission to modify requirements."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "DELETE":
        requirement.delete()

        return Response(
            {"message": "Requirement deleted successfully."},
            status=status.HTTP_200_OK
        )

    serializer = TenderRequirementSerializer(
        requirement,
        data=request.data,
        partial=(request.method == "PATCH")
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
