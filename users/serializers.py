from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models
from rest_framework import serializers

User: models.User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "phone", "password", "confirm_password", "role"]


    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
            
        if validated_data['role'] == User.Role.admin:
            validated_data["is_superuser"] = True
            validated_data["is_staff"] = True
        user = User.objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["role"] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["role"] = user.role

        return data


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role = serializers.CharField(source="get_role_display")

    class Meta:
        model = User
        fields = ("role", "full_name")

    def get_full_name(self, obj):
        return obj.get_users_full_name()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()