from django.urls import path
from . import views

app_name = 'billing'
urlpatterns = [
    path('accounts/', views.BillingListView.as_view(), name='billing'),
    path('', views.ChargeListView.as_view(), name='charges'),
]
