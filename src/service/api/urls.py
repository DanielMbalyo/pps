from django.urls import path
from . import views

app_name = 'shop_api'
urlpatterns = [
    path('', views.ShopListAPIView.as_view(), name='list'),
    path('create/', views.ShopCreateAPIView.as_view(), name='create'),
    path('<slug>/', views.ShopDetailAPIView.as_view(), name='detail'),
    path('<slug>/edit/', views.ShopUpdateAPIView.as_view(), name='update'),
    path('<slug>/delete/', views.ShopDeleteAPIView.as_view(), name='delete'),
]
