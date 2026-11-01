
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()


def get_user_data(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "role": user.role,
        "requested_role": user.requested_role,
        "role_request_status": user.role_request_status,
        "is_profile_complete": user.is_profile_complete,
    }


def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.role == User.Role.ADMIN
    )


# 1. USER REGISTRATION
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        try:
            send_mail(
                "Thank you for registering!",
                (
                    f"Hi {user.first_name},\n\n"
                    "Thank you for registering with our "
                    "AI Tender Compliance Platform.\n\n"
                    f"Your requested role is: {user.requested_role}\n"
                    "Your role request is awaiting Admin approval.\n\n"
                    "Regards,\n"
                    "AI Tender Compliance Platform Team"
                ),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            email_message = "Welcome email sent successfully."

        except Exception:
            email_message = "Account created, but email could not be sent."

        return Response(
            {
                "message": "Registration successful. Please log in.",
                "user": get_user_data(user),
                "email_status": email_message,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


# 2. USER LOGIN
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    serializer = CustomTokenObtainPairSerializer(
        data=request.data
    )

    if serializer.is_valid():

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )

    return Response(
        {"message": "Invalid email or password."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


# 3. JWT TOKEN REFRESH
@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_view(request):

    serializer = TokenRefreshSerializer(
        data=request.data
    )

    if serializer.is_valid():

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


# 4. LOGGED-IN USER DETAILS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):

    return Response(
        get_user_data(request.user),
        status=status.HTTP_200_OK,
    )


# 5. USER PROFILE
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_view(request):

    user = request.user

    if request.method == "GET":

        return Response(
            get_user_data(user),
            status=status.HTTP_200_OK,
        )

    allowed_fields = [
        "first_name",
        "last_name",
        "phone_number",
    ]

    for field in allowed_fields:

        if field in request.data:

            value = request.data[field]

            if not isinstance(value, str) or not value.strip():

                return Response(
                    {field: "This field cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            setattr(user, field, value.strip())

    user.is_profile_complete = bool(
        user.first_name.strip()
        and user.last_name.strip()
        and user.phone_number.strip()
    )

    user.save()

    return Response(
        {
            "message": "Profile updated successfully.",
            "user": get_user_data(user),
        },
        status=status.HTTP_200_OK,
    )


# 6. ADMIN: VIEW ROLE REQUESTS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def role_request_list_view(request):

    if not is_admin(request.user):

        return Response(
            {"error": "Only Admin can view role requests."},
            status=status.HTTP_403_FORBIDDEN,
        )

    users = User.objects.filter(
        role_request_status=User.RoleRequestStatus.PENDING
    ).order_by("date_joined")

    data = [
        get_user_data(user)
        for user in users
    ]

    return Response(
        {
            "total_pending_requests": len(data),
            "requests": data,
        },
        status=status.HTTP_200_OK,
    )


# 7. ADMIN: APPROVE OR REJECT ROLE REQUEST
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def role_request_decision_view(request, user_id):

    if not is_admin(request.user):

        return Response(
            {"error": "Only Admin can approve or reject role requests."},
            status=status.HTTP_403_FORBIDDEN,
        )

    target_user = User.objects.filter(
        id=user_id
    ).first()

    if target_user is None:

        return Response(
            {"error": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if target_user.role_request_status != User.RoleRequestStatus.PENDING:

        return Response(
            {"error": "This role request has already been processed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    decision = request.data.get("decision")

    if decision == "APPROVE":

        if not target_user.requested_role:
            return Response(
                {"error": "No requested role found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if target_user.requested_role == User.Role.ADMIN:
            return Response(
                {"error": "Admin role cannot be assigned through public registration."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target_user.role = target_user.requested_role

        target_user.role_request_status = (
            User.RoleRequestStatus.APPROVED
        )

        message = "User role approved successfully."

    elif decision == "REJECT":

        target_user.role_request_status = (
            User.RoleRequestStatus.REJECTED
        )

        message = "User role request rejected."

    else:

        return Response(
            {"error": "Decision must be APPROVE or REJECT."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    target_user.save()

    return Response(
        {
            "message": message,
            "user": get_user_data(target_user),
        },
        status=status.HTTP_200_OK,
    )


# 8. USER LOGOUT
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):

    return Response(
        {
            "message": (
                "Logout successful. Clear saved access and "
                "refresh tokens in the frontend."
            )
        },
        status=status.HTTP_200_OK,
    )
