
from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):
    message = "Only administrators can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and (
                user.is_superuser
                or user.role == "ADMIN"
            )
        )


class IsTenderManager(BasePermission):
    message = "Only tender managers can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role == "TENDER_MANAGER"
        )


class IsBidder(BasePermission):
    message = "Only bidders can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role == "BIDDER"
        )


class IsReviewer(BasePermission):
    message = "Only reviewers can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role == "REVIEWER"
        )


class IsTenderAuthority(BasePermission):
    message = "Only administrators and tender managers can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and (
                user.is_superuser
                or user.role in ["ADMIN", "TENDER_MANAGER"]
            )
        )


class IsReviewerOrAdmin(BasePermission):
    message = "Only reviewers and administrators can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and (
                user.is_superuser
                or user.role in ["ADMIN", "REVIEWER"]
            )
        )
