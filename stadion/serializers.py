from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from stadion.models import Stadium
from users.models import User
from django.contrib.gis.geos import Point

class StadiumSerializer(serializers.ModelSerializer):
    location = serializers.JSONField()
    distance = serializers.SerializerMethodField()
    class Meta:
        model = Stadium
        fields = (
            "id",
            "name",
            "address",
            "capacity",
            "guide",
            "region",
            "district",
            "zone_type",
            "price",
            "description",
            "opens_at",
            "closes_at",
            "created_time",
            "updated_time",
            "distance",
            "location"
        )

    def validate(self, attrs):
        request = self.context.get("request")
        if isinstance(request.user, User) and request.user.role == User.Role.customer:
            raise serializers.ValidationError(
                _("You have not permission to do this action")
            )
        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request")
        location_data = validated_data.pop('location')
        point = Point(float(location_data['lon']), float(location_data['lat']))
        validated_data["owner"] = request.user
        return Stadium.objects.create(location=point, **validated_data)
    
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        if location_data:
            instance.location = Point(float(location_data['lon']), float(location_data['lat']))
        return super().update(instance, validated_data)
    
    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["location"] = {
            'lon':instance.location.x,
            'lat':instance.location.y
        }
        return data