from django.urls import path
from . import views

app_name = 'product_api'
urlpatterns = [
    path('', views.ProductListAPIView.as_view(), name='list'),
    path('create/', views.ProductCreateAPIView.as_view(), name='create'),
    path('<slug>/', views.ProductDetailAPIView.as_view(), name='detail'),
    path('<slug>/edit/', views.ProductUpdateAPIView.as_view(), name='update'),
    path('<slug>/delete/', views.ProductDeleteAPIView.as_view(), name='delete'),
]
