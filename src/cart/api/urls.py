from django.urls import path

from .views import (
    CartAPIView,
    # CartClearAPIView,
    CartDeleteAPIView,
    CartUpdateAPIView,
    CheckoutAPIView,
    CheckoutFinalizeAPIView,
    ItemCountView,
)
app_name = 'cart_api'
urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('checkout/finalize/', CheckoutFinalizeAPIView.as_view(), name='checkout_finalize'),
    path('count/', ItemCountView.as_view(), name='count'),
    path('clear/', CartAPIView.as_view(), name='clear'),
    path('', CartAPIView.as_view(), name='list'),
    path('<product_id>/', CartDeleteAPIView.as_view(), name='delete'),
    path('<product_id>/<qty>/', CartUpdateAPIView.as_view(), name='update'),
]
