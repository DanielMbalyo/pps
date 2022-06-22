from django.urls import path
from . import views

app_name = 'product_api'
urlpatterns = [
    path('', views.ProductListAPIView.as_view(), name='all_list'),
    path('vendor/', views.UserProductListAPIView.as_view(), name='vendor_list'),
    path('create/', views.ProductCreateAPIView.as_view(), name='create'),
    path('<slug>/', views.ProductDetailAPIView.as_view(), name='detail'),
    path('<slug>/edit/', views.ProductUpdateAPIView.as_view(), name='update'),
]
