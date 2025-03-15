from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from stadion.serializers import StadiumSerializer
from stadion.models import Stadium
from users.models import User
from stadion.filters import StadiumFilterSet

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


start_time_param = openapi.Parameter(
    "start_time",
    openapi.IN_QUERY,
    description="Filter by start time",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATETIME,
)

end_time_param = openapi.Parameter(
    "end_time",
    openapi.IN_QUERY,
    description="Filter by end time",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATETIME,
)
longitude = openapi.Parameter(
    "longitude",
    openapi.IN_QUERY,
    description="Longitude coordinate",
    type=openapi.TYPE_NUMBER,
    format=openapi.FORMAT_FLOAT,
)

latitude = openapi.Parameter(
    "latitude",
    openapi.IN_QUERY,
    description="Latitude coordinate",
    type=openapi.TYPE_NUMBER,
    format=openapi.FORMAT_FLOAT,
)


class StadiumRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        request_user = self.request.user
        queryset = super().get_queryset()
        if (
            isinstance(request_user, User)
            and request_user.role == User.Role.stadium_owner
        ):
            return queryset.filter(owner=request_user)
        return super().get_queryset()


class StadiumListAPIView(ListAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = StadiumFilterSet
    search_fields = ["id", "name", "address", "guide"]

    def get_queryset(self):
        request_user = self.request.user
        queryset = super().get_queryset()
        if (
            isinstance(request_user, User)
            and request_user.role == User.Role.stadium_owner
        ):
            queryset = queryset.filter(owner=request_user)

        start_time = self.request.GET.get("start_time", None)
        end_time = self.request.GET.get("end_time", None)
        lat = self.request.query_params.get("latitude")
        lon = self.request.query_params.get("longitude")
        if start_time and end_time:
            queryset = queryset.exclude(
                bookings__start_time__lt=end_time, bookings__end_time__gt=start_time
            )
        if lat and lon:
            user_location = Point(float(lon), float(lat), srid=4326)
            queryset = queryset.annotate(
                distance=Distance("location", user_location)
            ).order_by("distance")
        return queryset

    @swagger_auto_schema(manual_parameters=[start_time_param, end_time_param, latitude, longitude])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class StadiumCreateAPIView(CreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
