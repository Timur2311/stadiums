from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from .models import District, Region
from .serializers import (
    DistrictsSerializer,
    RegionsSerializer,
)


class RegionsAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegionsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("=name",)
    queryset = Region.objects.all().order_by("-id")

   
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class DistrictsAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = DistrictsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("region__id",)
    search_fields = ("=name",)
    queryset = District.objects.all()


    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)