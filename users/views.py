from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from users.models import User
from users import serializers as users_serializers

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = users_serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = users_serializers.MyTokenObtainPairSerializer


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = users_serializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": _("You have successfully logged out")},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            raise ValidationError({"message": _("Invalid token")})
