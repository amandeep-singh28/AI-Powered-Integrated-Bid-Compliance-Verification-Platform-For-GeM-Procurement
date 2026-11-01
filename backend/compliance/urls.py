
from django.urls import path

from .views import (
    compliance_list_create,
    compliance_detail,
)

urlpatterns = [
    path(
        "",
        compliance_list_create,
        name="compliance-list-create"
    ),
    path(
        "<int:pk>/",
        compliance_detail,
        name="compliance-detail"
    ),
]
