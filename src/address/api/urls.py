from django.urls import path
from . import views

app_name = 'address_api'
urlpatterns = [
    path('', views.AddressListAPIView.as_view(), name='address_list'),
    path('create/', views.AddressCreateAPIView.as_view(), name='address_create'),
]
