
from django.urls import path
from .views import bid_list_create, bid_detail

urlpatterns = [
    path("", bid_list_create, name="bid-list-create"),
    path("<int:pk>/", bid_detail, name="bid-detail"),
]
