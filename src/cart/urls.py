from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartView.as_view(), name='list'),
    path('clear/', views.CartClearView.as_view(), name='clear'),
    path('update/<slug>/', views.CartUpdateView.as_view(), name='update'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', views.CheckoutDoneView.as_view(), name='success'),
]