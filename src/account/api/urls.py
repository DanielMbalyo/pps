from django.urls import path
from . import views

app_name = 'account_api'
urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('refresh_token/', views.LoginAPIView.as_view(), name='api_refresh_token'),
]
