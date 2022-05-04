from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('create/', views.ShopCreateView.as_view(), name="create"),
    path('', views.ShopListView.as_view(), name="list"),
    path('<slug>/', views.ShopView.as_view(), name="detail"),
    path('<slug>/update', views.ShopUpdateView.as_view(), name="update"),
]