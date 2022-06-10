from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('<order_id>', views.OrderDetailView.as_view(), name='detail'),
]
