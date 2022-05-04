from django.urls import path

from .views import (
    payment_method_view,
    payment_method_createview,
)

app_name = 'billing'
urlpatterns = [
    path('payment_method/', payment_method_view, name='billing-method'),
    path('payment_method/create/', payment_method_createview, name='billing-endpoint')
]
