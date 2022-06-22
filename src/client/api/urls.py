from django.urls import path
from . import views

app_name = 'client_api'
urlpatterns = [
    path('', views.ClientListAPIView.as_view(), name='list'),
    path('create/', views.ClientCreateAPIView.as_view(), name='create'),
    path('finance/', views.ClientFinanceAPIView.as_view(), name='finance'),
    path('<slug>/', views.ClientDetailAPIView.as_view(), name='detail'),
    path('<slug>/edit/', views.ClientUpdateAPIView.as_view(), name='update'),
]

