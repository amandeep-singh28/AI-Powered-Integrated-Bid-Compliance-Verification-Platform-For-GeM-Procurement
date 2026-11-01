
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Bid
from .serializers import BidSerializer
from tenders.models import Tender


def is_tender_authority(user):
    return user.is_superuser or user.role in ["ADMIN", "TENDER_MANAGER"]


def is_reviewer(user):
    return user.role == "REVIEWER"


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def bid_list_create(request):
    if request.method == "GET":
        if is_tender_authority(request.user) or is_reviewer(request.user):
            bids = Bid.objects.select_related("tender", "bidder").all()
        else:
            bids = Bid.objects.filter(
                bidder=request.user
            ).select_related("tender", "bidder")

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

    if request.user.role != "BIDDER":
        return Response(
            {"message": "Only bidders can submit bids."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = BidSerializer(data=request.data)

    if serializer.is_valid():
        tender = serializer.validated_data["tender"]

        if Bid.objects.filter(
            tender=tender,
            bidder=request.user,
        ).exists():
            return Response(
                {"message": "You have already submitted a bid for this tender."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bid = serializer.save(
            bidder=request.user,
            status=Bid.Status.SUBMITTED,
        )

        return Response(
            BidSerializer(bid).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bid_detail(request, pk):
    bid = get_object_or_404(
        Bid.objects.select_related("tender", "bidder"),
        pk=pk,
    )

    user = request.user

    if (
        bid.bidder_id != user.id
        and not is_tender_authority(user)
        and not is_reviewer(user)
    ):
        return Response(
            {"message": "You do not have permission to view this bid."},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response(BidSerializer(bid).data)
