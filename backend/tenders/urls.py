
from django.urls import path
from .views import tender_list_create, tender_detail

urlpatterns = [
    path("", tender_list_create, name="tender-list-create"),
    path("<int:pk>/", tender_detail, name="tender-detail"),
]
