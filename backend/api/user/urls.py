from django.urls import path
from .views import (
    Register, Logout, 
    CookieTokenObtainPairView, CookieTokenRefreshView,
)

urlpatterns = [
    path('auth/register', Register.as_view()),
    path('auth/logout', Logout.as_view()),
    path('auth/token', CookieTokenObtainPairView.as_view()),
    path('auth/token/refresh', CookieTokenRefreshView.as_view()),
]