from django.urls import path

from . import views

app_name = 'order_api'
urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='list'),
    path('<pk>/', views.OrderRetrieveAPIView.as_view(), name='detail'),
]
