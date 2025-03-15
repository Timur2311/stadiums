from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    path(
        "api/token/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path('api/register/', views.UserRegistrationAPIView.as_view(), name='register'),
]
