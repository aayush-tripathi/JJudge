from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView
urlpatterns = [
  path('auth/register', RegisterView.as_view()),
  path('auth/token', TokenObtainPairView.as_view()),
  path('auth/token/refresh', TokenRefreshView.as_view()),
]
