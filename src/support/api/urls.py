from django.urls import path
from . import views

app_name = 'support_api'
urlpatterns = [
    path('subscribe/', views.NewsletterAPIView.as_view(), name='subscribe'),
    path('contact/', views.ContactAPIView.as_view(), name='contact'),
]
