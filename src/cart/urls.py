from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('clear/<id>/', views.CartClearView.as_view(), name='clear'),
    path('update/<id>/<slug>/', views.CartUpdateView.as_view(), name='update'),
    path('remove/<id>/<slug>/', views.CartRemoveView.as_view(), name='remove'),
    path('checkout/<id>/', views.CheckoutView.as_view(), name='checkout'),
]