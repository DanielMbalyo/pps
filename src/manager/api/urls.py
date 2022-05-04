from django.urls import path

from .views import (
    UserCreateAPIView,
    UserLoginAPIView
    )
app_name = 'account_api'
urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='api_login'),
    path('register/', UserCreateAPIView.as_view(), name='api_register'),
]
