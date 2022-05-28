from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('home/', views.HomeView.as_view(), name='home'),
]