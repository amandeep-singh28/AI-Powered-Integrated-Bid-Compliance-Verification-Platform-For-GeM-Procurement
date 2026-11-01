
from django.urls import path

from .views import (
    report_list_create,
    report_detail,
)

urlpatterns = [
    path(
        "",
        report_list_create,
        name="report-list-create"
    ),
    path(
        "<int:pk>/",
        report_detail,
        name="report-detail"
    ),
]
