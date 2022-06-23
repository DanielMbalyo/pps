from django.urls import path

from . import views

app_name = 'order_api'
urlpatterns = [
    path('charges/', views.ChargeAPIView.as_view(), name='charge'),
    path('', views.BillingAPIView.as_view(), name='billing'),
]
