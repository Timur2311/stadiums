from django.urls import path

from .views import (
    BookingRetrieveDestroyAPIView, BookingCreateAPIView
)

urlpatterns = [
    path("", BookingCreateAPIView.as_view(), name="create_list"),
    path("<int:pk>/", BookingRetrieveDestroyAPIView.as_view(), name="retrieve_destroy_update"),
]
