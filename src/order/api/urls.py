from django.urls import path

from . import views

app_name = 'order_api'
urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='list'),
    path('<id>/', views.OrderRetrieveAPIView.as_view(), name='detail'),
    path('receive/<id>/<client>/', views.OrderReceiveAPIView.as_view(), name='receive'),
    path('complete/<id>/<client>/', views.OrderCompleteAPIView.as_view(), name='complete'),
]
