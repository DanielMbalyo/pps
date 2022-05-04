from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('billing/', views.BillingListView.as_view(), name='billing'),
    path('<order_id>', views.OrderDetailView.as_view(), name='detail'),
]
