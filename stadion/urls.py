from django.urls import path

from .views import (
    StadiumListAPIView,
    StadiumRetrieveUpdateDestroyAPIView,
    StadiumCreateAPIView,
)

urlpatterns = [
    path("", StadiumListAPIView.as_view(), name="list"),
    path("stadium/", StadiumCreateAPIView.as_view(), name="create"),
    path(
        "<int:pk>/",
        StadiumRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve_destroy_update",
    ),
]
