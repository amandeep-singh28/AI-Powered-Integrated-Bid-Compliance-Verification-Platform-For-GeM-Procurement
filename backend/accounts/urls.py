
from django.urls import path

from .views import (
    signup_view,
    login_view,
    logout_view,
    me_view,
    refresh_token_view,
    profile_view,
    role_request_list_view,
    role_request_decision_view,
)


urlpatterns = [

    # User Registration
    path(
        "register/",
        signup_view,
        name="register"
    ),

    # User Login
    path(
        "login/",
        login_view,
        name="login"
    ),

    # User Logout
    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    # Logged-in User Details
    path(
        "me/",
        me_view,
        name="me"
    ),

    # JWT Token Refresh
    path(
        "token/refresh/",
        refresh_token_view,
        name="token_refresh"
    ),

    # User Profile
    path(
        "profile/",
        profile_view,
        name="profile"
    ),

    # Admin: View Pending Role Requests
    path(
        "role-requests/",
        role_request_list_view,
        name="role-request-list"
    ),

    # Admin: Approve or Reject a Role Request
    path(
        "role-requests/<int:user_id>/",
        role_request_decision_view,
        name="role-request-decision"
    ),

]
