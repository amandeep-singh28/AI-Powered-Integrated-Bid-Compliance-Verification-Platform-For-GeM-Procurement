
from django.urls import path

from .views import (
    requirement_list_create,
    requirement_detail,
)

urlpatterns = [
    path(
        "",
        requirement_list_create,
        name="requirement-list-create"
    ),
    path(
        "<int:pk>/",
        requirement_detail,
        name="requirement-detail"
    ),
]
