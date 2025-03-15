from common.models import Region
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class RegionBaseSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    latitude = serializers.DecimalField(
        read_only=True, allow_null=True, max_digits=9, decimal_places=6
    )
    longitude = serializers.DecimalField(
        read_only=True, allow_null=True, max_digits=9, decimal_places=6
    )
    is_main = serializers.BooleanField(read_only=True)


class RegionsSerializer(RegionBaseSerializer):
    pass


class DistrictsSerializer(RegionBaseSerializer):
    pass


class RegionSerializer(serializers.Serializer):
    region = serializers.SlugRelatedField(
        slug_field="id", queryset=Region.objects.all()
    )

