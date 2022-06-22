from django.urls import path

from .views import (
    CartAPIView,
    CartClearAPIView,
    CartDeleteAPIView,
    CartUpdateAPIView,
    CheckoutAPIView,
)

app_name = 'cart_api'
urlpatterns = [
    path('checkout/<id>/', CheckoutAPIView.as_view(), name='checkout'),
    path('clear/<id>/', CartClearAPIView.as_view(), name='clear'),
    path('<id>/', CartAPIView.as_view(), name='list'),
    path('remove/<id>/<product_id>/', CartDeleteAPIView.as_view(), name='delete'),
    path('add/<id>/<product_id>/', CartUpdateAPIView.as_view(), name='update'),
]
