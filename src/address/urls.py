from django.urls import path
from .views import (
    AddressCreateView,
    AddressListView,
    AddressUpdateView,
    checkout_address_create_view,
    checkout_address_reuse_view,
    AccountBillingView,
    AccountReuseView,
    )
app_name = 'address'
urlpatterns = [
    path('', AddressListView.as_view(), name='list'),
    path('create/', AddressCreateView.as_view(), name='create'),
    path('<pk>/', AddressUpdateView.as_view(), name='update'),
    path('checkout/create/', checkout_address_create_view, name='checkout_create'),
    path('checkout/reuse/', checkout_address_reuse_view, name='checkout_reuse'),
    path('welcome/create/', AccountBillingView.as_view(), name='welcome_create'),
    path('welcome/reuse/', AccountReuseView.as_view(), name='welcome_create'),

]
