
from django.urls import path

from .views import (
    review_list_create,
    review_detail,
)

urlpatterns = [
    path(
        "",
        review_list_create,
        name="review-list-create"
    ),
    path(
        "<int:pk>/",
        review_detail,
        name="review-detail"
    ),
]

