from django.urls import path

from .views import (
    CartView,
    CartUpdateView,
    CheckoutView,
    CheckoutDoneView,
)

app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='list'),
    path('update/', CartUpdateView.as_view(), name='update'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', CheckoutDoneView.as_view(), name='success'),
]